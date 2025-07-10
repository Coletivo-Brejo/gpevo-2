@tool
extends Resource
class_name Operation

@export var params: Array[float]


static func create(
        _type: String,
        _params: Array[float],
    ) -> Operation:
    
    var operation: Operation
    if _type == LinearCombination.get_type():
        operation = LinearCombination.new()
    elif _type == ReLU.get_type():
        operation = ReLU.new()
    elif _type == NormalizedAtan.get_type():
        operation = NormalizedAtan.new()
    operation.params = _params
    return operation

static func from_dict(dict: Dictionary) -> Operation:
    var operation = Operation.create(
        dict["type"],
        dict["params"],
    )
    return operation

func to_dict() -> Dictionary:
    return {
        "type": get_type(),
        "params": params,
    }

static func get_type() -> String:
    return ""

func run(input: Array[float]) -> Array[float]:
    return input