@tool
extends Node2D

@onready var api: API = $API
@onready var masked_capsule: MaskedCapsule = $MaskedCapsule

@export var ship: ShipData
@export_tool_button("Save ship") var save_bt: Callable = save_ship
var container: Node2D


func _process(_delta: float) -> void:
    if ship != null:
        clear()
        container = Node2D.new()
        add_child(container)
        update_texture()
        update_flagella()
        update_sensors()

func update_texture() -> void:
    if ship != null:
        masked_capsule.texture = ship.chassis_texture

func update_flagella() -> void:
    if container != null and ship != null:
        for t in ship.thrusters:
            if t != null:
                var t_sprite = Sprite2D.new()
                t_sprite.set_texture(t.texture)
                t_sprite.set_z_index(-1)
                container.add_child(t_sprite)
                t_sprite.set_position(t.position)
                t_sprite.set_rotation(t.rotation)

func update_sensors() -> void:
    if container != null and ship != null:
        for s in ship.sensors:
            if s != null:
                var s_sprite = Sprite2D.new()
                s_sprite.set_texture(s.texture)
                container.add_child(s_sprite)
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
    if container != null:
        remove_child(container)
        container = null

func save_ship() -> void:
    api.save("/ships", ship.ship_id, ship)