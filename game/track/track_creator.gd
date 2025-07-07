@tool
extends Node2D

@onready var core_line: Line2D = $Track/Core
@onready var left_line: Line2D = $Track/LeftWall
@onready var right_line: Line2D = $Track/RightWall
@onready var track_api: TrackAPI = $TrackAPI

@export var track_id: String = ""
@export_tool_button("Load track") var load_bt: Callable = load_track
@export var track: TrackData
@export_tool_button("Save track") var save_bt: Callable = save_track


func _ready() -> void:
    track_api.track_loaded.connect(_on_track_loaded)

func _process(_delta: float) -> void:
    if track != null:
        track.compile_curves()
        update_lines()
    else:
        clear_lines()

func update_lines() -> void:
    core_line.set_points(track.core.get_baked_points())
    left_line.set_points(track.l_wall.get_baked_points())
    right_line.set_points(track.r_wall.get_baked_points())

func clear_lines() -> void:
    core_line.set_points([])
    left_line.set_points([])
    right_line.set_points([])

func save_track() -> void:
    track_api.save(track)

func load_track() -> void:
    track_api.load(track_id)

func _on_track_loaded(_track:TrackData) -> void:
    if _track != null:
        track = _track