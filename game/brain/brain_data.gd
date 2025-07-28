@tool
extends Resource
class_name BrainData

@export var neurons: Dictionary#[String, NeuronData]
var current_id: int
var layers: Array


static func create(
		_neurons: Array[NeuronData] = [],
		_current_id: int = 0,
		_layers: Array = [],
	) -> BrainData:
	
	var brain = BrainData.new()
	brain.neurons = {}
	for n in _neurons:
		brain.neurons[n.neuron_id] = n
	brain.create_connections()
	brain.current_id = _current_id
	brain.layers = _layers
	return brain

static func from_dict(dict: Dictionary) -> BrainData:
	var _neurons: Array[NeuronData] = []
	for s in dict["neurons"]:
		_neurons.append(NeuronData.from_dict(s))
	var brain = BrainData.create(
		_neurons,
		dict["current_id"],
		dict["layers"],
	)
	return brain

func to_dict() -> Dictionary:
	var _neurons: Array[Dictionary] = []
	for n in neurons:
		_neurons.append(neurons[n].to_dict())
	return {
		"neurons": _neurons,
		"current_id": current_id,
		"layers": layers,
	}

func create_connections() -> void:
	for n in neurons:
		var neuron: NeuronData = neurons[n]
		neuron.input = []
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

func create_input_neuron(neuron_id: String) -> NeuronData:
	var neuron = NeuronData.create(
		neuron_id,
		0,
		[],
		[],
	)
	neurons[neuron_id] = neuron
	return neuron

func create_output_neuron(neuron_id: String) -> NeuronData:
	var operations: Array[Operation] = []
	operations.append(Operation.create(
		"linear_combination",
		[0.],
	))
	operations.append(Operation.create(
		"normalized_atan",
		[0., 1.],
	))
	var neuron = NeuronData.create(
		neuron_id,
		-1,
		[],
		operations,
	)
	neurons[neuron_id] = neuron
	return neuron

func create_hidden_neuron(b: float = 0., leakage: float = .01) -> NeuronData:
	var neuron_id: String = get_next_id()
	var operations: Array[Operation] = []
	operations.append(Operation.create(
		"linear_combination",
		[b],
	))
	operations.append(Operation.create(
		"relu",
		[leakage],
	))
	var neuron = NeuronData.create(
		neuron_id,
		-1,
		[],
		operations,
	)
	neurons[neuron_id] = neuron
	return neuron
