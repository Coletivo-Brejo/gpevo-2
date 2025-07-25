extends Resource
class_name TrainingData

@export var training_id: String
@export var racer_id: String
@export var setups: Array[TrainingRunSetup]
@export var save_results: bool
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
@export var prob_create_neuron: float
@export var prob_delete_neuron: float
@export var prob_create_connection: float
@export var prob_delete_connection: float
var run_history: Array
var clone_history: Array[String]
var elapsed_time: float
var end_reason: String


static func create(
        _training_id: String,
        _racer_id: String,
        _setups: Array[TrainingRunSetup],
        _save_results: bool,
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
        _prob_create_neuron: float,
        _prob_delete_neuron: float,
        _prob_create_connection: float,
        _prob_delete_connection: float,
    ) -> TrainingData:

    var training = TrainingData.new()
    training.training_id = _training_id
    training.racer_id = _racer_id
    training.setups = _setups
    training.save_results = _save_results
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
    training.prob_create_neuron = _prob_create_neuron
    training.prob_delete_neuron = _prob_delete_neuron
    training.prob_create_connection = _prob_create_connection
    training.prob_delete_connection = _prob_delete_connection
    return training

static func from_dict(dict: Dictionary) -> TrainingData:
    var _setups: Array[TrainingRunSetup] = []
    for t in dict["setups"]:
        _setups.append(TrainingRunSetup.from_dict(t))

    var training = TrainingData.create(
        dict["training_id"],
        dict["racer_id"],
        _setups,
        dict["save_results"],
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
        dict["prob_create_neuron"],
        dict["prob_delete_neuron"],
        dict["prob_create_connection"],
        dict["prob_delete_connection"],
    )
    return training

func to_dict() -> Dictionary:
    var _runs: Array = []
    for it in run_history:
        _runs.append([])
        for r_data in it:
            _runs[-1].append(r_data.to_dict())
    return {
        "training_id": training_id,
        "racer_id": racer_id,
        "setups": Serializer.from_list(setups),
        "save_results": save_results,
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
        "prob_create_neuron": prob_create_neuron,
        "prob_delete_neuron": prob_delete_neuron,
        "prob_create_connection": prob_create_connection,
        "prob_delete_connection": prob_delete_connection,
        "run_history": _runs,
        "clone_history": clone_history,
        "elapsed_time": elapsed_time,
        "end_reason": end_reason,
    }