@tool
extends Resource
class_name ShipData

@export var ship_id: String
@export var name: String
@export var mass: float:
    set(value): mass = value; emit_changed()
@export var chassis_texture: Texture2D:
    set(value): chassis_texture = value; emit_changed()
@export var thrusters: Array[ThrusterData]
@export var sensors: Array[SensorSetData]


static func create(
        _ship_id: String,
        _name: String,
        _mass: float,
        _chassis_texture: Texture2D,
        _thrusters: Array[ThrusterData],
        _sensors: Array[SensorSetData],
    ) -> ShipData:

    var ship = ShipData.new()
    ship.ship_id = _ship_id
    ship.name = _name
    ship.mass = _mass
    ship.chassis_texture = _chassis_texture
    ship.thrusters = _thrusters
    ship.sensors = _sensors
    return ship

static func from_dict(dict: Dictionary) -> ShipData:
    var _thrusters: Array[ThrusterData] = []
    for t in dict["thrusters"]:
        _thrusters.append(ThrusterData.from_dict(t))
    var _sensors: Array[SensorSetData] = []
    for s in dict["sensors"]:
        _sensors.append(SensorSetData.from_dict(s))
    var ship = ShipData.create(
        dict["ship_id"],
        dict["name"],
        dict["mass"],
        Serializer.to_texture(dict["chassis_texture"]),
        _thrusters,
        _sensors,
    )
    return ship

func to_dict() -> Dictionary:
    return {
        "ship_id": ship_id,
        "name": name,
        "mass": mass,
        "chassis_texture": Serializer.from_texture(chassis_texture),
        "thrusters": Serializer.from_list(thrusters),
        "sensors": Serializer.from_list(sensors),
    }