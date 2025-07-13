@tool
extends Resource
class_name NeuronData

@export var neuron_id: String
@export var max_inputs: int
@export var input_ids: Array[String]
@export var operations: Array[Operation]
var activation: float
var activated: bool
var input: Array[NeuronData]


static func create(
        _neuron_id: String,
        _max_inputs: int,
        _input_ids: Array[String],
        _operations: Array[Operation],
    ) -> NeuronData:

    var neuron = NeuronData.new()
    neuron.neuron_id = _neuron_id
    neuron.max_inputs = _max_inputs
    neuron.input_ids = _input_ids
    neuron.operations = _operations
    neuron.activation = 0.
    neuron.activated = false
    #neuron.input = []
    return neuron

static func from_dict(dict: Dictionary) -> NeuronData:
    var _input_ids: Array[String] = []
    for i in dict["input_ids"]:
        _input_ids.append(i)
    var _operations: Array[Operation] = []
    for op in dict["operations"]:
        _operations.append(Operation.from_dict(op))
    var neuron = NeuronData.create(
        dict["neuron_id"],
        dict["max_inputs"],
        _input_ids,
        _operations,
    )
    return neuron

func to_dict() -> Dictionary:
    return {
        "neuron_id": neuron_id,
        "max_inputs": max_inputs,
        "input_ids": input_ids,
        "operations": Serializer.from_list(operations),
    }
    
func activate() -> float:
    if not activated:
        var z: Array[float] = []
        for n in input:
            z.append(n.activate())
        for op in operations:
            z = op.run(z)
        activation = z[0]
        activated = true
    return activation

func activate_manually(value: float) -> void:
    activation = value
    activated = true