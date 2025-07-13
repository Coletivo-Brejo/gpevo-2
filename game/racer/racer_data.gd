@tool
extends Resource
class_name RacerData

@export var racer_id: String
@export var name: String
@export var brain: BrainData
@export var ship: ShipData


static func create(
        _racer_id: String,
        _name: String,
        _brain: BrainData,
        _ship: ShipData,
    ) -> RacerData:

    var racer = RacerData.new()
    racer.racer_id = _racer_id
    racer.name = _name
    racer.brain = _brain
    racer.ship = _ship
    return racer

static func from_dict(dict: Dictionary) -> RacerData:
    var racer = RacerData.create(
        dict["racer_id"],
        dict["name"],
        BrainData.from_dict(dict["brain"]),
        ShipData.from_dict(dict["ship"]),
    )
    return racer

func to_dict() -> Dictionary:
    return {
        "racer_id": racer_id,
        "name": name,
        "brain": brain.to_dict(),
        "ship": ship.to_dict(),
    }