@tool
extends Node2D

@onready var ship_api: ShipAPI = $ShipAPI

@export var transparent_sprite: bool:
    set(value):
        transparent_sprite = value
        modulate_color = "#FFFFFF77" if value else "#FFFFFF"
@export var ship_id: String = ""
@export_tool_button("Load ship") var load_bt: Callable = load_ship
@export var ship: ShipData
@export_tool_button("Save ship") var save_bt: Callable = save_ship
var ship_sprite: Sprite2D
var modulate_color: Color


func _ready() -> void:
    ship_api.ship_loaded.connect(_on_ship_loaded)
    transparent_sprite = false

func _process(_delta: float) -> void:
    if ship != null:
        update_ship()

func update_ship() -> void:
    if ship_sprite != null:
        clear()
    if ship != null:
        ship_sprite = Sprite2D.new()
        ship_sprite.set_texture(ship.chassis_texture)
        ship_sprite.set_modulate(modulate_color)
        add_child(ship_sprite)
        for t in ship.thrusters:
            if t != null:
                var t_sprite = Sprite2D.new()
                t_sprite.set_texture(t.texture)
                t_sprite.set_z_index(-1)
                ship_sprite.add_child(t_sprite)
                t_sprite.set_position(t.position)
                t_sprite.set_rotation(t.rotation)
        for s in ship.sensors:
            if s != null:
                var s_sprite = Sprite2D.new()
                s_sprite.set_texture(s.texture)
                ship_sprite.add_child(s_sprite)
                s_sprite.set_position(s.position)
                s_sprite.set_rotation(s.rotation)
                var step: float = 0.
                if s.amount > 1:
                    step = s.aperture/(s.amount-1)
                for i in s.amount:
                    var point = Vector2.UP*s.reach
                    if s.amount > 1:
                        point = point.rotated(-s.aperture/2. + i*step)
                    var line = Line2D.new()
                    line.set_width(2.)
                    line.set_default_color(Color("#000000"))
                    s_sprite.add_child(line)
                    line.set_points([Vector2.ZERO, point])

func clear() -> void:
    if ship_sprite != null:
        remove_child(ship_sprite)
        ship_sprite.queue_free()
        ship_sprite = null

func save_ship() -> void:
    ship_api.save(ship)

func load_ship() -> void:
    ship_api.load(ship_id)

func _on_ship_loaded(_ship:ShipData) -> void:
    if _ship != null:
        ship = _ship