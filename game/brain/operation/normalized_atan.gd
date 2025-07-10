@tool
extends Operation
class_name NormalizedAtan


static func get_type() -> String:
    return "normalized_atan"

func run(input: Array[float]) -> Array[float]:
    var min_value: float = params[0]
    var max_value: float = params[1]
    var delta: float = max_value - min_value
    var z: float = input[0]
    z = (atan(z) + PI/2.) / PI
    z = z*delta + min_value
    return [z]