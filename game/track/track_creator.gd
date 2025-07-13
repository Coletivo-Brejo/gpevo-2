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


func _ready() -> void:
    if Engine.is_editor_hint():
        api.resource_loaded.connect(_on_track_loaded)
    else:
        clear_lines()
        if track != null:
            track.compile_curves()
        var game_track = Track.create(track)
        add_child(game_track)

func _process(_delta: float) -> void:
    if Engine.is_editor_hint():
        if track != null:
            track.compile_curves()
            update_lines()
        else:
            clear_lines()
    else:
        camera.set_position(dummy.position)

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