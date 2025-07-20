extends Resource
class_name TrainingData

@export var training_id: String
@export var track_id: String
@export var racer_id: String
@export var save_results: bool
@export var run_data: RunData
@export var n_neighbors: int
@export var initial_temperature: float
@export var cooling_rate: float
@export var convergence_threshold: float
@export var convergence_iterations: int
@export var n_iterations: int
@export var progress_objective: float
@export var time_objective: float
@export var max_training_time: float
@export var greedy: bool
var run_history: Array[RunData]
var racer_history: Array[RunStats]
var elapsed_time: float
var end_reason: String


static func create(
        _training_id: String,
        _track_id: String,
        _racer_id: String,
        _save_results: bool,
        _run_data: RunData,
        _n_neighbors: int,
        _initial_temperature: float,
        _cooling_rate: float,
        _convergence_threshold: float,
        _convergence_iterations: int,
        _n_iterations: int,
        _progress_objective: float,
        _time_objective: float,
        _max_training_time: float,
        _greedy: bool,
    ) -> TrainingData:

    var training = TrainingData.new()
    training.training_id = _training_id
    training.track_id = _track_id
    training.racer_id = _racer_id
    training.save_results = _save_results
    training.run_data = _run_data
    training.n_neighbors = _n_neighbors
    training.initial_temperature = _initial_temperature
    training.cooling_rate = _cooling_rate
    training.convergence_threshold = _convergence_threshold
    training.convergence_iterations = _convergence_iterations
    training.n_iterations = _n_iterations
    training.progress_objecive = _progress_objective
    training.time_objective = _time_objective
    training.max_training_time = _max_training_time
    training.greedy = _greedy
    return training

static func from_dict(dict: Dictionary) -> TrainingData:
    var training = TrainingData.create(
        dict["training_id"],
        dict["track_id"],
        dict["racer_id"],
        dict["save_results"],
        RunData.from_dict(dict["run_data"]),
        dict["n_neighbors"],
        dict["initial_temperature"],
        dict["cooling_rate"],
        dict["convergence_threshold"],
        dict["convergence_iterations"],
        dict["n_iterations"],
        dict["progress_objective"],
        dict["time_objective"],
        dict["max_training_time"],
        dict["greedy"],
    )
    return training

func to_dict() -> Dictionary:
    return {
        "training_id": training_id,
        "track_id": track_id,
        "racer_id": racer_id,
        "save_results": save_results,
        "run_data": run_data.to_dict(),
        "n_neighbors": n_neighbors,
        "initial_temperature": initial_temperature,
        "cooling_rate": cooling_rate,
        "convergence_threshold": convergence_threshold,
        "convergence_iterations": convergence_iterations,
        "n_iterations": n_iterations,
        "progress_objective": progress_objective,
        "time_objective": time_objective,
        "max_training_time": max_training_time,
        "greedy": greedy,
        "run_history": Serializer.from_list(run_history),
        "racer_history": Serializer.from_list(racer_history),
        "elapsed_time": elapsed_time,
        "end_reason": end_reason,
    }