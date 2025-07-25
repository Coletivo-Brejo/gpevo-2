extends Node2D
class_name Training

signal training_finished

@onready var api: API = $API
@onready var run_container: Control = $CanvasLayer/Runs

@export var data: TrainingData
var runs_data: Array[RunData]
var runs: Array[Run]
var runs_vp: Array[SubViewport]
var runs_finished: Array[bool]
var iteration: int
var convergence_iteration: int
var temperature: float
var current_racer: RacerData
var current_clone_id: String
var neighbors: Array[RacerData]
var all_loaded: bool
var running: bool


func _ready() -> void:
	for setup in data.setups:
		var run_data = RunData.create(
			"",
			null,
			[],
			setup.run_setup,
		)
		runs_data.append(run_data)
		var vp_container = SubViewportContainer.new()
		vp_container.set_stretch(true)
		vp_container.set_custom_minimum_size(Vector2(get_viewport().size.x/data.setups.size(), 0.))
		run_container.add_child(vp_container)
		var vp = SubViewport.new()
		vp_container.add_child(vp)
		runs_vp.append(vp)
	data.elapsed_time = 0.
	iteration = 0
	convergence_iteration = 0
	temperature = data.initial_temperature
	all_loaded = false
	running = false
	if not data.setups.is_empty():
		load_track(data.setups[0].track_id)

func _process(_delta: float) -> void:
	if all_loaded and not running:
		run_iteration()
		running = true

func run_iteration() -> void:
	create_neighbors()
	start_runs()

func create_neighbors() -> void:
	neighbors = []
	neighbors.append(current_racer)
	for i in data.n_neighbors:
		var neighbor: RacerData = current_racer.clone()
		neighbor.racer_id = "clone_%d" % i
		var rng: float = randf()
		var accum_prob_create_neuron: float = data.prob_create_neuron
		var accum_prob_delete_neuron: float = data.prob_delete_neuron + accum_prob_create_neuron
		var accum_prob_create_connection: float = data.prob_create_connection + accum_prob_delete_neuron
		var accum_prob_delete_connection: float = data.prob_delete_connection + accum_prob_create_connection
		print("Mutation RNG: %.2f\nProbs: %.2f, %.2f, %.2f, %.2f" % [
			rng,
			accum_prob_create_neuron,
			accum_prob_delete_neuron,
			accum_prob_create_connection,
			accum_prob_delete_connection
		])
		if accum_prob_create_neuron > rng:
			neighbor.brain.mutate_creating_neuron()
		elif accum_prob_delete_neuron > rng:
			neighbor.brain.mutate_deleting_neuron()
		elif accum_prob_create_connection > rng:
			neighbor.brain.mutate_creating_connection()
		elif accum_prob_delete_connection > rng:
			neighbor.brain.mutate_removing_connection()
		else:
			neighbor.brain.mutate_weights()
		neighbors.append(neighbor)

func start_runs() -> void:
	for run in runs:
		if run != null:
			run.queue_free()
	runs = []
	for i in data.setups.size():
		var run_data: RunData = runs_data[i].clone()
		run_data.run_id = "%s_run%d_it%02d" % [data.training_id, i, iteration]
		run_data.racers_data = neighbors
		var run = Run.create(run_data)
		run.run_finished.connect(_on_run_finished)
		runs_vp[i].add_child(run)
		runs.append(run)

func load_track(track_id: String) -> void:
	api.resource_loaded.connect(_on_track_loaded)
	api.load("/tracks", track_id)

func _on_track_loaded(track_dict: Dictionary) -> void:
	api.resource_loaded.disconnect(_on_track_loaded)
	if track_dict != null:
		var track_data = TrackData.from_dict(track_dict)
		for i in data.setups.size():
			if data.setups[i].track_id == track_data.track_id:
				runs_data[i].track_data = track_data
	var all_tracks_loaded: bool = true
	for i in data.setups.size():
		if runs_data[i].track_data == null:
			all_tracks_loaded = false
			load_track(data.setups[i].track_id)
			break
	if all_tracks_loaded:
		load_racer(data.racer_id)

func load_racer(racer_id: String) -> void:
	api.resource_loaded.connect(_on_racer_loaded)
	api.load("/racers", data.racer_id)

func _on_racer_loaded(racer_dict: Dictionary) -> void:
	api.resource_loaded.disconnect(_on_racer_loaded)
	current_racer = RacerData.from_dict(racer_dict)
	all_loaded = true

func _on_run_finished() -> void:
	for run in runs:
		if not run.data.finished:
			return
	var run_times: Array[float] = []
	for run in runs:
		run_times.append(run.data.elapsed_time)
	data.elapsed_time += run_times.max()
	data.run_history.append([])
	for run in runs:
		data.run_history[-1].append(run.data)
	evaluate_and_select()
	var previous_progress: float = get_result_for_racer(data.racer_id)
	var current_progress: float = get_result_for_racer(current_clone_id)
	var improvement_ratio: float = current_progress/previous_progress
	if improvement_ratio < (1. + data.convergence_threshold):
		convergence_iteration += 1
	else:
		convergence_iteration = 0
	var end_reason: String = get_ending_reason()
	if end_reason != "":
		end_training(end_reason)
	else:
		temperature *= (1. - data.cooling_rate)
		iteration += 1
		run_iteration()

func get_result_for_racer(racer_id: String) -> float:
	var result: float = 99999999.
	for run in runs:
		var stat: RunStats = run.data.get_racer_stats(racer_id)
		result = min(stat.progress, result)
	return result

func evaluate_and_select() -> void:
	var progress_deltas: Array[float] = []
	var best_progress: float = get_result_for_racer(data.racer_id)
	var best_racer: RacerData = null
	for i in data.n_neighbors:
		var progress: float = get_result_for_racer("clone_%d" % i)
		progress_deltas.append(best_progress - progress)
		if data.greedy and progress > best_progress:
			best_progress = progress
			best_racer = runs[0].data.racers_data[i+1]
	print(progress_deltas)
	if best_racer != null:
		set_new_racer(best_racer)
	else:
		var accum_probs: Array[float] = []
		for i in range(progress_deltas.size()):
			var prob: float = exp(-progress_deltas[i]/temperature)
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
	current_racer.racer_id = data.racer_id

func get_ending_reason() -> String:
	var current_progress: float = get_result_for_racer(current_clone_id)
	if data.progress_objective > 0. and current_progress > data.progress_objective:
			return "progress objetive met"
	# elif data.time_objective > 0. and stat.finished and stat.time < data.time_objective:
	# 	return "time objetive met"
	elif data.convergence_iterations > 0 and convergence_iteration >= data.convergence_iterations:
		return "improvement converged"
	elif data.max_training_time > 0. and data.elapsed_time > data.max_training_time:
		return "max training time reached"
	elif iteration >= data.n_iterations-1:
		return "max iteration reached"
	else:
		return ""

func end_training(reason: String) -> void:
	data.end_reason = reason
	print(reason)
	if data.save_results:
		save_results()
	else:
		finish_training()

func finish_training() -> void:
	training_finished.emit()

func save_results() -> void:
	api.resource_saved.connect(_on_results_saved)
	api.save("/trainings", data.training_id, data)

func _on_results_saved() -> void:
	api.resource_saved.disconnect(_on_results_saved)
	api.save("/racers", data.racer_id, current_racer)

func _on_racer_updated() -> void:
	api.resource_saved.disconnect(_on_racer_updated)
	finish_training()
