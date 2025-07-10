@tool
extends Operation
class_name LinearCombination


static func get_type() -> String:
    return "linear_combination"

func run(input: Array[float]) -> Array[float]:
    var a: float = 0.
    for i in input.size():
        a += input[i]*params[i]
    return [a]