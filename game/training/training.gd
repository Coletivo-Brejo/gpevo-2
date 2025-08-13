extends Node2D
class_name Training

signal training_finished(reason: String)
signal training_interrupted(reason: String)

const scene_path: String = "res://training/training.tscn"

@onready var api: API = $API
@onready var run_container: Control = $CanvasLayer/Runs
@onready var label: Label = $CanvasLayer/Label
@onready var game_over: Control = find_child("GameOver")
@onready var game_over_lb: Label = find_child("GameOverLb")

@export var data: TrainingData
var runs_data: Array[RunData]
var runs: Array[Run]
var runs_vp: Array[SubViewport]
var runs_finished: Array[bool]
var frozen_progress: Dictionary
var current_racer: RacerData
var current_clone_id: String
var neighbors: Array[RacerData]
var all_loaded: bool
var all_saved: bool
var running: bool
var finished: bool
var label_info: Dictionary


static func create(
		_data: TrainingData,
	) -> Training:
	var training: Training = load(scene_path).instantiate()
	training.data = _data
	return training

func _ready() -> void:
	for setup in data.setup.setups:
		var run_data = RunData.create(
			"",
			null,
			[],
			setup.run_setup,
		)
		runs_data.append(run_data)
		var vp_container = SubViewportContainer.new()
		vp_container.set_stretch(true)
		vp_container.set_custom_minimum_size(Vector2(get_viewport().size.x/data.setup.setups.size(), 0.))
		run_container.add_child(vp_container)
		var vp = SubViewport.new()
		vp_container.add_child(vp)
		runs_vp.append(vp)
	all_loaded = false
	all_saved = true
	running = false
	if not data.setup.setups.is_empty():
		load_track(data.setup.setups[0].track_id)
	label_info["Versão"] = "v%s" % ProjectSettings.get_setting("application/config/version")
	training_interrupted.connect(show_game_over)
	training_finished.connect(show_game_over)

func _process(_delta: float) -> void:
	if all_loaded and all_saved and not finished:
		if data.end_reason != "":
			finished = true
			finish_training()
		elif not running:
			running = true
			run_iteration()

func run_iteration() -> void:
	label_info["Iteração"] = data.iteration + 1
	label_info["Tempo decorrido"] = "%.0fs" % data.elapsed_time
	update_label()
	create_neighbors()
	start_runs()

func create_neighbors() -> void:
	neighbors = [current_racer]
	var mutation_request_body: Dictionary = {
		"brain": current_racer.brain.to_dict(),
		"mutation_setup": data.setup.mutation_setup.to_dict(),
	}
	api.post_responded.connect(_on_brains_received)
	api.post("/mutate", mutation_request_body)

func _on_brains_received(brains_response: Variant) -> void:
	var brains: Array[Dictionary] = []
	brains.assign(brains_response)
	api.post_responded.disconnect(_on_brains_received)
	for i in brains.size():
		var brain_dict: Dictionary = brains[i]
		var clone: RacerData = current_racer.clone()
		clone.racer_id = "clone_%d" % i
		clone.brain = BrainData.from_dict(brain_dict)
		neighbors.append(clone)
	start_runs()

func start_runs() -> void:
	for run in runs:
		if run != null:
			run.queue_free()
	runs = []
	for i in data.setup.setups.size():
		var run_data: RunData = runs_data[i].clone()
		run_data.run_id = "%s_run%d_it%02d" % [data.training_id, i, data.iteration]
		var duplicated_clones: Array[RacerData] = []
		for n in neighbors:
			duplicated_clones.append(n.clone())
		run_data.racers_data = duplicated_clones
		var run = Run.create(run_data)
		run.run_finished.connect(_on_run_finished)
		run.first_finished.connect(_on_first_finished.bind(run_data.run_id))
		runs_vp[i].add_child(run)
		runs.append(run)

func load_track(track_id: String) -> void:
	api.resource_loaded.connect(_on_track_loaded)
	api.load("/tracks", track_id)

func _on_track_loaded(track_dict: Dictionary) -> void:
	api.resource_loaded.disconnect(_on_track_loaded)
	if track_dict != null:
		var track_data = TrackData.from_dict(track_dict)
		for i in data.setup.setups.size():
			if data.setup.setups[i].track_id == track_data.track_id:
				runs_data[i].track_data = track_data
	var all_tracks_loaded: bool = true
	for i in data.setup.setups.size():
		if runs_data[i].track_data == null:
			all_tracks_loaded = false
			load_track(data.setup.setups[i].track_id)
			break
	if all_tracks_loaded:
		load_racer(data.setup.racer_id)

func load_racer(racer_id: String) -> void:
	api.resource_loaded.connect(_on_racer_loaded)
	api.load("/racers", data.setup.racer_id)

func _on_racer_loaded(racer_dict: Dictionary) -> void:
	api.resource_loaded.disconnect(_on_racer_loaded)
	current_racer = RacerData.from_dict(racer_dict)
	data.brain_history.append(current_racer.brain)
	all_loaded = true

func _on_run_finished() -> void:
	for run in runs:
		if not run.data.finished:
			return
	for run in runs:
		if not run.data.run_id in frozen_progress:
			freeze_progress(run)
	var run_times: Array[float] = []
	for run in runs:
		run_times.append(run.data.elapsed_time)
	data.elapsed_time += run_times.max()
	data.run_id_history.append([])
	for run in runs:
		data.run_id_history[-1].append(run.data.run_id)
	evaluate_and_select()
	var previous_progress: float = get_result_for_racer(data.setup.racer_id)
	var current_progress: float = get_result_for_racer(current_clone_id)
	var improvement_ratio: float = current_progress/previous_progress
	if improvement_ratio < (1. + data.setup.convergence_threshold):
		data.convergence_iteration += 1
	else:
		data.convergence_iteration = 0
	var end_reason: String = get_ending_reason()
	if end_reason != "":
		end_training(end_reason)
	else:
		data.temperature *= (1. - data.setup.cooling_rate)
		data.iteration += 1
		if data.setup.save_results:
			save_results()
		else:
			run_iteration()

func _on_first_finished(run_id: String) -> void:
	var run: Run = null
	for r in runs:
		if r.data.run_id == run_id:
			run = r
			break
	if run != null:
		freeze_progress(run)

func freeze_progress(run: Run) -> void:
	var progress_dict: Dictionary = {}
	for stat in run.data.stats:
		progress_dict[stat.racer_data.racer_id] = stat.progress
	frozen_progress[run.data.run_id] = progress_dict

func get_result_for_racer(racer_id: String) -> float:
	var result: float = 99999999.
	for run_id in frozen_progress:
		result = minf(frozen_progress[run_id][racer_id], result)
	# for run in runs:
	# 	var stat: RunStats = run.data.get_racer_stats(racer_id)
	# 	result = min(stat.progress, result)
	return result

func evaluate_and_select() -> void:
	var progress_deltas: Array[float] = []
	var best_progress: float = get_result_for_racer(data.setup.racer_id)
	var best_racer: RacerData = null
	for i in data.setup.mutation_setup.n_clones:
		var progress: float = get_result_for_racer("clone_%d" % i)
		progress_deltas.append(best_progress - progress)
		if data.setup.greedy and progress > best_progress:
			best_progress = progress
			best_racer = runs[0].data.racers_data[i+1]
	print(progress_deltas)
	if best_racer != null:
		set_new_racer(best_racer)
	else:
		var accum_probs: Array[float] = []
		for i in range(progress_deltas.size()):
			var prob: float = exp(-progress_deltas[i]/data.temperature)
			if i == 0:
				accum_probs.append(prob)
			else:
				accum_probs.append(prob+accum_probs[i-1])
		for i in accum_probs.size():
			accum_probs[i] /= accum_probs[-1]
		var rng: float = randf()
		print(accum_probs)
		print(rng)
		for i in range(accum_probs.size()):
			if accum_probs[i] >= rng:
				set_new_racer(runs[0].data.racers_data[i+1])
				break

func set_new_racer(racer_data: RacerData) -> void:
	current_racer = racer_data.clone()
	current_clone_id = current_racer.racer_id
	data.clone_history.append(current_clone_id)
	data.brain_history.append(current_racer.brain)
	current_racer.racer_id = data.setup.racer_id

func get_ending_reason() -> String:
	var current_progress: float = get_result_for_racer(current_clone_id)
	if data.setup.progress_objective > 0. and current_progress > data.setup.progress_objective:
			return "progress objetive met"
	# elif data.setup.time_objective > 0. and stat.finished and stat.time < data.setup.time_objective:
	# 	return "time objetive met"
	elif data.setup.convergence_iterations > 0 and data.convergence_iteration >= data.setup.convergence_iterations:
		return "improvement converged"
	elif data.setup.max_training_time > 0. and data.elapsed_time > data.setup.max_training_time:
		return "max training time reached"
	elif data.iteration >= data.setup.n_iterations-1:
		return "max iteration reached"
	else:
		return ""

func end_training(reason: String) -> void:
	data.end_reason = reason
	print(reason)
	if data.setup.save_results:
		save_results()
	else:
		finish_training()

func finish_training() -> void:
	training_finished.emit(data.end_reason)

func save_results() -> void:
	print("Salvando treinamento")
	all_saved = false
	running = false
	var update_body: Dictionary = {}
	update_body["training"] = data.to_dict()
	update_body["runs"] = []
	for run in runs:
		update_body["runs"].append(run.data.to_dict())
	update_body["brain"] = current_racer.brain.to_dict()
	api.post_responded.connect(_on_results_saved)
	api.post("/trainings/%s/save_iteration" % data.training_id, update_body)

func _on_results_saved(body: Variant) -> void:
	api.post_responded.disconnect(_on_results_saved)
	if "Erro" in body:
		training_interrupted.emit(body["Erro"])
	else:
		all_saved = true

func update_label() -> void:
	var label_text: String = ""
	for info in label_info:
		label_text += "%s: %s\n" % [info, label_info[info]]
	label.set_text(label_text)

func show_game_over(reason: String) -> void:
	var text: String = game_over_lb.text
	text += "\n%s" % reason
	game_over_lb.set_text(text)
	game_over.set_visible(true)