@tool
extends Operation
class_name ReLU


static func get_type() -> String:
    return "relu"

func run(input: Array[float]) -> Array[float]:
    var leakage: float = params[0]
    var z: float = input[0]
    return [maxf(leakage*z, z)]