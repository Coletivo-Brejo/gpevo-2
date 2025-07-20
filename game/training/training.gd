extends Node2D
class_name Training

signal training_finished

@onready var api: API = $API

@export var data: TrainingData
var iteration: int
var convergence_iteration: int
var temperature: float
var current_racer: RacerData
var neighbors: Array[RacerData]
var run: Run
var all_loaded: bool


func _ready() -> void:
	data.elapsed_time = 0.
	iteration = 0
	convergence_iteration = 0
	temperature = data.initial_temperature
	all_loaded = false
	api.resource_loaded.connect(_on_track_loaded)
	api.load("/tracks", data.track_id)

func _process(_delta: float) -> void:
	if all_loaded:
		run_iteration()
		all_loaded = false

func run_iteration() -> void:
	create_neighbors()
	start_run()

func create_neighbors() -> void:
	neighbors = []
	neighbors.append(current_racer)
	for i in data.n_neighbors:
		var neighbor: RacerData = current_racer.clone()
		neighbor.racer_id = "clone_%d" % i
		var mutable_neurons: Array[NeuronData] = neighbor.brain.get_neurons_with_linear_combination()
		mutable_neurons.shuffle()
		neighbor.brain.mutate_weights_from_neuron(mutable_neurons[0])
		neighbors.append(neighbor)

func start_run() -> void:
	if run != null:
		run.queue_free()
	var run_data: RunData = data.run_data.clone()
	run_data.run_id = "%s_it%d" % [data.training_id, iteration]
	run_data.racers_data = neighbors
	run = Run.create(run_data, true)
	run.run_ended.connect(_on_run_finished)
	add_child(run)

func _on_track_loaded(track_dict: Dictionary) -> void:
	api.resource_loaded.disconnect(_on_track_loaded)
	if track_dict != null:
		print(track_dict.keys())
		var track_data = TrackData.from_dict(track_dict)
		data.run_data.track_data = track_data
		api.resource_loaded.connect(_on_racer_loaded)
		api.load("/racers", data.racer_id)

func _on_racer_loaded(racer_dict: Dictionary) -> void:
	api.resource_loaded.disconnect(_on_racer_loaded)
	current_racer = RacerData.from_dict(racer_dict)
	all_loaded = true

func _on_run_finished() -> void:
	data.elapsed_time += run.data.elapsed_time
	data.run_history.append(run.data)
	if iteration == 0:
		data.racer_history.append(run.data.stats[0])
		var stat: RunStats = run.data.stats[0]
		print("Progress: %.0f - Finished: %s - Time: %.1f" % [stat.progress, stat.finished, stat.time])
	evaluate_and_select()
	var improvement_ratio: float = data.racer_history[-1].progress/data.racer_history[-2].progress
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

func evaluate_and_select() -> void:
	var stats: Array[RunStats] = run.data.stats
	var progress_deltas: Array[float] = []
	var best_progress: float = stats[0].progress
	var best_stat: RunStats = null
	for s in stats.slice(1):
		progress_deltas.append(stats[0].progress - s.progress)
		if data.greedy and s.progress > best_progress:
			best_stat = s
			best_progress = s.progress
	print(progress_deltas)
	if best_stat != null:
		set_new_racer(best_stat)
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
				set_new_racer(stats[i+1])
				break

func set_new_racer(stat: RunStats) -> void:
	current_racer = stat.racer_data
	current_racer.racer_id = data.racer_id
	data.racer_history.append(stat)
	print("Progress: %.0f - Finished: %s - Time: %.1f" % [stat.progress, stat.finished, stat.time])

func get_ending_reason() -> String:
	var stat: RunStats = data.racer_history[-1]
	if data.progress_objective > 0. and stat.progress > data.progress_objective:
			return "progress objetive met"
	elif data.time_objective > 0. and stat.finished and stat.time < data.time_objective:
		return "time objetive met"
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
