@tool
extends Node2D

@onready var api: API = $API

@export var racer_id: String = ""
@export_tool_button("Load racer") var load_bt: Callable = load_racer
@export var ship_id: String = ""
@export_tool_button("load ship") var load_ship_bt: Callable = load_ship
@export var racer: RacerData
@export_tool_button("Create brain") var create_brain_bt: Callable = create_brain
@export_tool_button("Save racer") var save_bt: Callable = save_racer


func _ready() -> void:
    pass

func create_brain() -> void:
    if racer != null and racer.ship != null:
        var brain = BrainData.create()
        var current_sensor: int = 0
        for s in racer.ship.sensors:
            for i in s.amount:
                brain.create_input_neuron("s%d" % current_sensor)
                current_sensor += 1
        for i in 3:
            brain.create_input_neuron("v%d" % i)
        for i in racer.ship.thrusters.size():
            brain.create_output_neuron("t%d" % i)
        racer.brain = brain

func save_racer() -> void:
    api.save("/racers", racer.racer_id, racer)

func load_racer() -> void:
    api.resource_loaded.connect(_on_racer_loaded)
    api.load("/racers", racer_id)

func _on_racer_loaded(racer_dict: Dictionary) -> void:
    api.resource_loaded.disconnect(_on_racer_loaded)
    if racer_dict != null:
        racer = RacerData.from_dict(racer_dict)

func load_ship() -> void:
    api.resource_loaded.connect(_on_ship_loaded)
    api.load("/ships", ship_id)

func _on_ship_loaded(ship_dict: Dictionary) -> void:
    api.resource_loaded.disconnect(_on_ship_loaded)
    if ship_dict != null:
        var ship = ShipData.from_dict(ship_dict)
        if racer != null:
            racer.ship = ship