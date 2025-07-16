extends CharacterBody2D
class_name Racer

const scene_path: String = "res://racer/racer.tscn"
const LINEAR_DAMP: float = .1
const ANGULAR_DAMP: float = .1

@onready var collision: CollisionPolygon2D = $Collision

@export var data: RacerData
var paused: bool = false
var thrusters: Array[Thruster]
var sensors: Array[Sensor]
var inertia: float
var linear_accel: Vector2
var angular_accel: float
var angular_velocity: float


static func create(
    _data: RacerData,
        ) -> Racer:
    var racer: Racer = load(scene_path).instantiate()
    racer.data = _data
    return racer

func _ready() -> void:
    collision.set_polygon(data.ship.chassis_collision)
    calculate_inertia()
    build_ship()
    draw_ship()
    data.brain.create_connections()

func _physics_process(delta: float) -> void:
    velocity *= (1. - LINEAR_DAMP*delta)
    angular_velocity *= (1. - ANGULAR_DAMP*delta)
    data.brain.refresh()
    sense()
    thrust()
    rotation += angular_velocity * delta
    move_and_slide()

func set_paused(_paused: bool) -> void:
    set_process(!_paused)
    set_physics_process(!_paused)
    paused = _paused

func calculate_inertia() -> void:
    var w: float = data.ship.chassis_texture.get_width()
    var h: float = data.ship.chassis_texture.get_height()
    inertia = data.ship.mass * (w*w + h*h) / 12.

func build_ship() -> void:
    for t in data.ship.thrusters:
        if t != null:
            var thruster = Thruster.create()
            add_child(thruster)
            thruster.set_position(t.position)
            thruster.set_rotation(t.rotation)
            thrusters.append(thruster)
    for s in data.ship.sensors:
        if s != null:
            var step: float = 0.
            if s.amount > 1:
                step = s.aperture/(s.amount-1)
            for i in s.amount:
                var sensor = Sensor.create(s.reach)
                add_child(sensor)
                sensor.set_rotation(s.rotation)
                if s.amount > 1:
                    sensor.rotate(-s.aperture/2. + i*step)
                sensor.set_position(s.position)
                sensors.append(sensor)

func draw_ship() -> void:
    var ship_sprite = Sprite2D.new()
    ship_sprite.set_texture(data.ship.chassis_texture)
    add_child(ship_sprite)
    for t in data.ship.thrusters:
        if t != null:
            var t_sprite = Sprite2D.new()
            t_sprite.set_texture(t.texture)
            t_sprite.set_z_index(-1)
            ship_sprite.add_child(t_sprite)
            t_sprite.set_position(t.position)
            t_sprite.set_rotation(t.rotation)
    for s in data.ship.sensors:
        if s != null:
            var s_sprite = Sprite2D.new()
            s_sprite.set_texture(s.texture)
            ship_sprite.add_child(s_sprite)
            s_sprite.set_position(s.position)
            s_sprite.set_rotation(s.rotation)

func sense() -> void:
    for i in sensors.size():
        var neuron_id: String = "s%d" % i
        var neuron: NeuronData = data.brain.neurons[neuron_id]
        var sensor: Sensor = sensors[i]
        var reading: float = sensor.get_reading()
        neuron.activate_manually(reading)
    var x_neuron: NeuronData = data.brain.neurons["v0"]
    var y_neuron: NeuronData = data.brain.neurons["v1"]
    var ang_neuron: NeuronData = data.brain.neurons["v2"]
    x_neuron.activate_manually(velocity.x)
    y_neuron.activate_manually(-velocity.y)
    ang_neuron.activate_manually(angular_velocity)

func thrust() -> void:
    var total_force = Vector2.ZERO
    var tau: float = 0.
    for i in thrusters.size():
        var neuron_id: String = "t%d" % i
        var neuron: NeuronData = data.brain.neurons[neuron_id]
        var intensity: float = neuron.activate()
        var thruster: Thruster = thrusters[i]
        thruster.thrust(intensity)
        var thruster_data: ThrusterData = data.ship.thrusters[i]
        var direction: Vector2 = Vector2.UP.rotated(thruster_data.rotation)
        var force: Vector2 = direction * thruster_data.power * intensity
        total_force += force
        tau += thruster.position.cross(force)
    linear_accel = (total_force / data.ship.mass).rotated(rotation)
    velocity += linear_accel
    angular_accel = tau / inertia
    angular_velocity += angular_accel