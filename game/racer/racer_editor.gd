@tool
extends Node2D

@onready var api: API = $API

@export var racer_id: String = ""
@export_tool_button("Load racer") var load_bt: Callable = load_racer
@export var ship_id: String = ""
@export_tool_button("load ship") var load_ship_bt: Callable = load_ship
@export var racer: RacerData
@export_tool_button("Create brain") var create_brain_bt: Callable = create_brain
@export_tool_button("Fully connect") var fully_connect_bt: Callable = fully_connect_brain
@export_tool_button("Save racer") var save_bt: Callable = save_racer


func _ready() -> void:
    pass

func create_brain() -> void:
    if racer != null and racer.ship != null:
        var brain = BrainData.create()
        brain.layers = [[], []]
        var current_sensor: int = 0
        for s in racer.ship.sensors:
            for i in s.amount:
                var n_id: String = "s%d" % current_sensor
                brain.create_input_neuron(n_id)
                brain.layers[1].append(n_id)
                current_sensor += 1
        for i in 3:
            var n_id: String = "v%d" % i
            brain.create_input_neuron(n_id)
            brain.layers[1].append(n_id)
        for i in racer.ship.thrusters.size():
            var n_id: String = "t%d" % i
            brain.create_output_neuron(n_id)
            brain.layers[0].append(n_id)
        racer.brain = brain

func fully_connect_brain() -> void:
    if racer != null and racer.brain != null:
        for n in racer.brain.neurons:
            if not n.begins_with("t"):
                continue
            print("connecting neurons to %s" % n)
            var neuron: NeuronData = racer.brain.neurons[n]
            for n0 in racer.brain.neurons:
                if n0.begins_with("t"):
                    continue
                print("connecting %s" % n0)
                var input: NeuronData = racer.brain.neurons[n0]
                neuron.input_ids.append(n0)
                neuron.input.append(input)
                neuron.operations[0].params.append(0.)

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