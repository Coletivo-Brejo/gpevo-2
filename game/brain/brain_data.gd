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
    for n in _neurons:
        for i in n.input_ids:
            n.input.append(brain.neurons[i])
    brain.current_id = _current_id
    return brain

static func from_dict(dict: Dictionary) -> BrainData:
    var brain = BrainData.create(
        dict["neurons"],
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

func refresh() -> void:
    for n in neurons:
        var neuron: NeuronData = neurons[n]
        neuron.activated = false