@tool
extends Resource
class_name BrainData

@export var neurons: Dictionary#[String, NeuronData]
var current_id: int


static func create(
		_neurons: Array[NeuronData] = [],
		_current_id: int = 0,
	) -> BrainData:
	
	var brain = BrainData.new()
	brain.neurons = {}
	for n in _neurons:
		brain.neurons[n.neuron_id] = n
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

func get_neurons_with_linear_combination() -> Array[NeuronData]:
	var _neurons: Array[NeuronData]
	for n in neurons:
		var neuron: NeuronData = neurons[n]
		for op in neuron.operations:
			if op is LinearCombination:
				_neurons.append(neuron)
	return _neurons

func mutate_weights(
		amount: int = 1,
		std: float = 1.,
		weight_amount: int = 1,
	) -> void:
	for i in amount:
		var neurons_with_weights: Array[NeuronData] = []
		for n in neurons:
			var neuron: NeuronData = neurons[n]
			if neuron.operations[0] is LinearCombination:
				neurons_with_weights.append(neuron)
		if not neurons_with_weights.is_empty():
			var neuron: NeuronData = neurons_with_weights.pick_random()
			mutate_weights_from_neuron(neuron, std, weight_amount)

func mutate_weights_from_neuron(
		neuron: NeuronData,
		std: float = 1.,
		amount: int = -1
	) -> void:
	var lin_op: LinearCombination
	for op in neuron.operations:
		if op is LinearCombination:
			lin_op = op
			break
	if lin_op != null:
		var w_idx: Array = range(lin_op.params.size())
		w_idx.shuffle()
		if amount == -1:
			amount = lin_op.params.size()
		for i in amount:
			lin_op.params[w_idx[i]] += randfn(0., std)

func mutate_weights_from_neuron_id(
		neuron_id: String,
		std: float = 1.,
		amount: int = -1
	) -> void:
	mutate_weights_from_neuron(neurons[neuron_id], std, amount)

func mutate_removing_connection(
		amount: int = 1,
	) -> void:
	for i in amount:
		var neurons_with_input: Array[NeuronData] = []
		for n in neurons:
			var neuron: NeuronData = neurons[n]
			if not neuron.input.is_empty():
				neurons_with_input.append(neuron)
		if not neurons_with_input.is_empty():
			var neuron: NeuronData = neurons_with_input.pick_random()
			remove_random_input_from_neuron(neuron)
		else:
			return

func remove_random_input_from_neuron(
		neuron: NeuronData,
		amount: int = 1,
	) -> void:
	for i in amount:
		var input_idx: int = randi_range(0, neuron.input.size()-1)
		remove_input_from_neuron(neuron, input_idx)
		if neuron.input.is_empty():
			return

func remove_input_from_neuron(
		neuron: NeuronData,
		input_idx: int,
	) -> void:
	if input_idx in range(neuron.input.size()):
		neuron.input_ids.remove_at(input_idx)
		neuron.input.remove_at(input_idx)
		neuron.operations[0].params.remove_at(input_idx+1)

func mutate_creating_connection(
		amount: int = 1,
		std: float = 1.,
	) -> void:
	for i in amount:
		var possible_inputs: Array[NeuronData] = []
		for n in neurons:
			var input_n: NeuronData = neurons[n]
			if not get_possible_connections_from_input(input_n).is_empty():
				possible_inputs.append(input_n)
		if not possible_inputs.is_empty():
			var input_n: NeuronData = possible_inputs.pick_random()
			var possible_outputs: Array[NeuronData] = get_possible_connections_from_input(input_n)
			var output_n: NeuronData = possible_outputs.pick_random()
			connect_neurons(output_n, input_n, std)
		else:
			return

func get_possible_connections_from_input(
		input_n: NeuronData,
	) -> Array[NeuronData]:
	var possible_connections: Array[NeuronData] = []
	if not input_n.neuron_id.begins_with("t"): # thrusters não podem ser input
		for n in neurons:
			var output_n: NeuronData = neurons[n]
			if output_n == input_n:
				continue
			elif input_n in output_n.input:
				continue
			elif output_n.max_inputs != -1 and output_n.input.size() >= output_n.max_inputs:
				continue
			elif output_n in get_recursive_inputs(input_n): # impede conexões cíclicas
				continue
			possible_connections.append(output_n)
	return possible_connections

func get_recursive_inputs(
		neuron: NeuronData,
	) -> Array[NeuronData]:
	var all_inputs: Array[NeuronData] = []
	for input_n in neuron.input:
		if input_n not in all_inputs:
			all_inputs.append(input_n)
			all_inputs.append_array(get_recursive_inputs(input_n))
	return all_inputs

func connect_neurons(
		output_n: NeuronData,
		input_n: NeuronData,
		std: float = 1.,
	) -> void:
	output_n.input_ids.append(input_n.neuron_id)
	output_n.input.append(input_n)
	output_n.operations[0].params.append(randfn(0., std))

func delete_neuron(neuron: NeuronData) -> void:
	var neuron_id: String = neuron.neuron_id
	delete_neuron_from_id(neuron_id)

func delete_neuron_from_id(neuron_id: String) -> void:
	if neuron_id in neurons.keys():
		for n in neurons:
			var output: NeuronData = neurons[n]
			var input_idx: int = output.input_ids.find(neuron_id)
			if input_idx == -1:
				continue
			else:
				remove_input_from_neuron(output, input_idx)
		neurons.erase(neuron_id)