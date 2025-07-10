@tool
extends Resource
class_name NeuronData

@export var neuron_id: String
@export var max_inputs: int
@export var input_neurons: Array[String]
@export var operations: Array[Operation]
var activation: float
var activated: bool
var brain: BrainData


static func create(
        _neuron_id: String,
        _max_inputs: int,
        _input_neurons: Array[String],
        _operations: Array[Operation],
    ) -> NeuronData:

    var neuron = NeuronData.new()
    neuron.neuron_id = _neuron_id
    neuron.max_inputs = _max_inputs
    neuron.input_neurons = _input_neurons
    neuron.operations = _operations
    return neuron

static func from_dict(dict: Dictionary) -> NeuronData:
    var _operations: Array[Operation] = []
    for op in dict["operations"]:
        _operations.append(Operation.from_dict(op))
    var neuron = NeuronData.create(
        dict["neuron_id"],
        dict["max_inputs"],
        dict["input_neurons"],
        _operations,
    )
    return neuron

func to_dict() -> Dictionary:
    return {
        "neuron_id": neuron_id,
        "max_inputs": max_inputs,
        "input_neurons": input_neurons,
        "operations": Serializer.from_list(operations),
    }
    
func activate() -> float:
    if not activated:
        var z: Array[float] = []
        for n in input_neurons:
            var input: NeuronData = brain.find(n)
            z.append(input.activate())
        for op in operations:
            z = op.run(z)
        activation = z[0]
        activated = true
    return activation

func activate_manually(value: float) -> void:
    activation = value
    activated = true