extends Node2D
class_name Thruster

const scene_path: String = "res://racer/thruster.tscn"

@onready var particles: CPUParticles2D = $Particles

@export var max_velocity: float
var min_velocity: float
var intensity: float


static func create() -> Thruster:
    var thruster: Thruster = load(scene_path).instantiate()
    return thruster

func _ready() -> void:
    min_velocity = particles.initial_velocity_min

func thrust(_intensity: float) -> void:
    intensity = _intensity
    particles.set_emitting(intensity > 0.)
    particles.set_param_max(
        CPUParticles2D.PARAM_INITIAL_LINEAR_VELOCITY,
        intensity*(max_velocity-min_velocity)
    )