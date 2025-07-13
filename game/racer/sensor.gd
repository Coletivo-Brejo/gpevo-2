extends RayCast2D
class_name Sensor

const scene_path: String = "res://racer/sensor.tscn"

@onready var line: Line2D = $Line


static func create(
    _reach: float,
        ) -> Sensor:
    var sensor: Sensor = load(scene_path).instantiate()
    sensor.set_target_position(Vector2.UP*_reach)
    return sensor

func _ready() -> void:
    pass

func _process(_delta: float) -> void:
    if enabled and is_colliding():
        set_modulate(Color.WHITE)
        line.set_point_position(1, to_local(get_collision_point()))
    else:
        set_modulate(Color("#ffffff33"))
        line.set_visible(false)

func get_reading() -> float:
    var reading: float = 0.
    if is_colliding():
        var distance: float = to_local(get_collision_point()).length()
        var max_distance: float = target_position.length()
        reading = (max_distance-distance) / max_distance
    return reading