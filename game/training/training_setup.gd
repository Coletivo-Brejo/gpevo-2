extends Resource
class_name TrainingSetup

@export var racer_id: String
@export var setups: Array[TrainingRunSetup]
@export var save_results: bool
@export var initial_temperature: float
@export var cooling_rate: float
@export var convergence_threshold: float
@export var convergence_iterations: int
@export var n_iterations: int
@export var progress_objective: float
@export var time_objective: float
@export var max_training_time: float
@export var greedy: bool
@export var mutation_setup: MutationSetup

static func create(
        _racer_id: String,
        _setups: Array[TrainingRunSetup],
        _save_results: bool,
        _initial_temperature: float,
        _cooling_rate: float,
        _convergence_threshold: float,
        _convergence_iterations: int,
        _n_iterations: int,
        _progress_objective: float,
        _time_objective: float,
        _max_training_time: float,
        _greedy: bool,
        _mutation_setup: MutationSetup,
    ) -> TrainingSetup:

    var training = TrainingSetup.new()
    training.racer_id = _racer_id
    training.setups = _setups
    training.save_results = _save_results
    training.initial_temperature = _initial_temperature
    training.cooling_rate = _cooling_rate
    training.convergence_threshold = _convergence_threshold
    training.convergence_iterations = _convergence_iterations
    training.n_iterations = _n_iterations
    training.progress_objecive = _progress_objective
    training.time_objective = _time_objective
    training.max_training_time = _max_training_time
    training.greedy = _greedy
    training.mutation_setup = _mutation_setup
    return training

static func from_dict(dict: Dictionary) -> TrainingSetup:
    var _setups: Array[TrainingRunSetup] = []
    for t in dict["setups"]:
        _setups.append(TrainingRunSetup.from_dict(t))
    var training = TrainingSetup.create(
        dict["racer_id"],
        _setups,
        dict["save_results"],
        dict["initial_temperature"],
        dict["cooling_rate"],
        dict["convergence_threshold"],
        dict["convergence_iterations"],
        dict["n_iterations"],
        dict["progress_objective"],
        dict["time_objective"],
        dict["max_training_time"],
        dict["greedy"],
        dict["mutation_setup"],
    )
    return training

func to_dict() -> Dictionary:
    return {
        "racer_id": racer_id,
        "setups": Serializer.from_list(setups),
        "save_results": save_results,
        "initial_temperature": initial_temperature,
        "cooling_rate": cooling_rate,
        "convergence_threshold": convergence_threshold,
        "convergence_iterations": convergence_iterations,
        "n_iterations": n_iterations,
        "progress_objective": progress_objective,
        "time_objective": time_objective,
        "max_training_time": max_training_time,
        "greedy": greedy,
        "mutation_setup": mutation_setup.to_dict(),
    }