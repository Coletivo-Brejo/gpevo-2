@tool
extends Resource
class_name BrainData

@export var neurons: Dictionary#[String, NeuronData]
var current_id: int


static func create(
		_neurons: Array[NeuronData],
		_current_id: int
	) -> BrainData:
	
	var brain = BrainData.new()
	brain.neurons = {}
	for n in _neurons:
		brain.neurons[n.neuron_id] = n
		n.input = []
	brain.create_connections()
	brain.current_id = _current_id
	return brain

static func from_dict(dict: Dictionary) -> BrainData:
	var _neurons: Array[NeuronData] = []
	for s in dict["neurons"]:
		_neurons.append(NeuronData.from_dict(s))
	var brain = BrainData.create(
		_neurons,
		dict["current_id"],
	)
	return brain

func to_dict() -> Dictionary:
	var _neurons: Array[Dictionary] = []
	for n in neurons:
		_neurons.append(neurons[n].to_dict())
	return {
		"neurons": _neurons,
		"current_id": current_id,
	}

func create_connections() -> void:
	for n in neurons:
		var neuron: NeuronData = neurons[n]
		for i in neuron.input_ids:
			neuron.input.append(neurons[i])

func refresh() -> void:
	for n in neurons:
		var neuron: NeuronData = neurons[n]
		neuron.activated = false

func get_next_id() -> String:
	var next_id: String = "n%d" % current_id
	current_id += 1
	return next_id
