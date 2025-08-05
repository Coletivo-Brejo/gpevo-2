extends Resource
class_name TrainingData

@export var training_id: String
@export var setup: TrainingSetup
var iteration: int
var convergence_iteration: int
@export var temperature: float
var run_id_history: Array
var clone_history: Array[String]
var brain_history: Array[BrainData]
var elapsed_time: float
var end_reason: String


static func create(
		_training_id: String,
		_setup: TrainingSetup,
		_iteration: int,
		_convergence_iteration: int,
		_temperature: float,
		_run_id_history: Array,
		_clone_history: Array[String],
		_brain_history: Array[BrainData],
		_elapsed_time: float,
		_end_reason: String,
	) -> TrainingData:
	var training = TrainingData.new()
	training.training_id = _training_id
	training.setup = _setup
	training.iteration = _iteration
	training.convergence_iteration = _convergence_iteration
	training.temperature = _temperature
	training.run_id_history = _run_id_history
	training.clone_history = _clone_history
	training.brain_history = _brain_history
	training.elapsed_time = _elapsed_time
	training.end_reason = _end_reason
	return training

static func from_dict(dict: Dictionary) -> TrainingData:
	var _clones: Array[String] = []
	_clones.assign(dict["clone_history"])
	var _brains: Array[BrainData] = []
	for b in dict["brain_history"]:
		_brains.append(BrainData.from_dict(b))
	var training = TrainingData.create(
		dict["training_id"],
		TrainingSetup.from_dict(dict["setup"]),
		dict["iteration"],
		dict["convergence_iteration"],
		dict["temperature"],
		dict["run_id_history"],
		_clones,
		_brains,
		dict["elapsed_time"],
		dict["end_reason"],
	)
	return training

func to_dict() -> Dictionary:
	return {
		"training_id": training_id,
		"setup": setup.to_dict(),
		"iteration": iteration,
		"convergence_iteration": convergence_iteration,
		"temperature": temperature,
		"run_id_history": run_id_history,
		"clone_history": clone_history,
		"brain_history": Serializer.from_list(brain_history),
		"elapsed_time": elapsed_time,
		"end_reason": end_reason,
	}
