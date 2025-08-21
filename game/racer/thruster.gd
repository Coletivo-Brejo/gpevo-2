extends Node2D
class_name Thruster

const scene_path: String = "res://racer/thruster.tscn"

@onready var sprite: Sprite2D = $Sprite
@onready var animation_player: AnimationPlayer = $AnimationPlayer

@export var max_wiggle_speed: float
@export var min_wiggle_speed: float
var intensity: float


static func create() -> Thruster:
    var thruster: Thruster = load(scene_path).instantiate()
    return thruster

func _ready() -> void:
    animation_player.play("wiggle")
    animation_player.set_speed_scale(0.)

func thrust(_intensity: float) -> void:
    intensity = _intensity
    var wiggle_speed: float = intensity * (max_wiggle_speed - min_wiggle_speed)
    animation_player.set_speed_scale(wiggle_speed)