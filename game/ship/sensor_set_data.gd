@tool
extends Resource
class_name SensorSetData

@export_range(1, 10) var amount: int
@export_range(0., 180., 1., "radians_as_degrees") var aperture: float
@export_range(0., 500., 10.) var reach: float
@export var texture: Texture2D
@export var position: Vector2
@export_range(-180., 180., 1., "radians_as_degrees") var rotation: float


static func create(
        _amount: int,
        _aperture: float,
        _reach: float,
        _texture: Texture2D,
        _position: Vector2,
        _rotation: float,
    ) -> SensorSetData:

    var sensor = SensorSetData.new()
    sensor.amount = _amount
    sensor.aperture = _aperture
    sensor.reach = _reach
    sensor.texture = _texture
    sensor.position = _position
    sensor.rotation = _rotation
    return sensor

static func from_dict(dict: Dictionary) -> SensorSetData:
    var sensor = SensorSetData.create(
        dict["amount"],
        dict["aperture"],
        dict["reach"],
        Serializer.to_texture(dict["texture"]),
        Serializer.to_vector2(dict["position"]),
        dict["rotation"],
    )
    return sensor

func to_dict() -> Dictionary:
    return {
        "amount": amount,
        "aperture": aperture,
        "reach": reach,
        "texture": Serializer.from_texture(texture),
        "position": Serializer.from_vector2(position),
        "rotation": rotation,
    }