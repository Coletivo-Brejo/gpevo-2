@tool
extends Node2D

@onready var core_line: Line2D = $EditorTrack/Core
@onready var left_line: Line2D = $EditorTrack/LeftWall
@onready var right_line: Line2D = $EditorTrack/RightWall
@onready var api: API = $API
@onready var camera: Camera2D = $Camera
@onready var dummy: CharacterBody2D = $Dummy

@export var track_id: String = ""
@export_tool_button("Load track") var load_bt: Callable = load_track
@export var track: TrackData
@export_tool_button("Save track") var save_bt: Callable = save_track
@export_group("Test drive")
@export var racer_data: RacerData
var racer: Racer
var racer_label: Label


func _ready() -> void:
    if Engine.is_editor_hint():
        api.resource_loaded.connect(_on_track_loaded)
    else:
        clear_lines()
        var game_track = Track.create(track)
        add_child(game_track)
        if racer_data != null:
            racer = Racer.create(racer_data)
            add_child(racer)
            racer_label = Label.new()
            camera.add_child(racer_label)

func _process(_delta: float) -> void:
    if Engine.is_editor_hint():
        if track != null:
            track.compile_curves()
            update_lines()
        else:
            clear_lines()
    else:
        camera.set_position(dummy.position)
        if racer_label != null:
            var racer_report: String = """
            Velocity: %.2f, %.2f
            Acceleration: %.2f, %.2f
            Angular velocity: %.2f
            Angular acceleration: %.2f
            t0: %.2f
            t1: %.2f
            s1: %.2f
            s3: %.2f
            """ % [
                racer.velocity.x,
                racer.velocity.y,
                racer.linear_accel.x,
                racer.linear_accel.y,
                racer.angular_velocity,
                racer.angular_accel,
                racer.data.brain.neurons["t0"].activation,
                racer.data.brain.neurons["t1"].activation,
                racer.data.brain.neurons["s1"].activation,
                racer.data.brain.neurons["s3"].activation,
            ]
            racer_label.set_text(racer_report)

func update_lines() -> void:
    core_line.set_points(track.core.get_baked_points())
    left_line.set_points(track.l_wall.get_baked_points())
    right_line.set_points(track.r_wall.get_baked_points())

func clear_lines() -> void:
    core_line.set_points([])
    left_line.set_points([])
    right_line.set_points([])

func save_track() -> void:
    api.save("/tracks", track.track_id, track)

func load_track() -> void:
    api.load("/tracks", track_id)

func _on_track_loaded(track_dict: Dictionary) -> void:
    if track_dict != null:
        track = TrackData.from_dict(track_dict)