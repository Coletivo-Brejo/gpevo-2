@tool
extends Resource
class_name ThrusterData

@export var power: float:
    set(value): power = value; emit_changed()
@export var texture: Texture2D:
    set(value): texture = value; emit_changed()
@export var position: Vector2:
    set(value): position = value; emit_changed()
@export_range(-180., 180., 1., "radians_as_degrees") var rotation: float:
    set(value): rotation = value; emit_changed()


static func create(
        _power: float,
        _texture: Texture2D,
        _position: Vector2,
        _rotation: float,
    ) -> ThrusterData:

    var thruster = ThrusterData.new()
    thruster.power = _power
    thruster.texture = _texture
    thruster.position = _position
    thruster.rotation = _rotation
    return thruster

static func from_dict(dict: Dictionary) -> ThrusterData:
    var thruster = ThrusterData.create(
        dict["power"],
        Serializer.to_texture(dict["texture"]),
        Serializer.to_vector2(dict["position"]),
        dict["rotation"],
    )
    return thruster

func to_dict() -> Dictionary:
    return {
        "power": power,
        "texture": Serializer.from_texture(texture),
        "position": Serializer.from_vector2(position),
        "rotation": rotation,
    }