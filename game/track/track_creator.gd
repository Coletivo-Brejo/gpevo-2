@tool
extends Node2D

@onready var core_line:Line2D = $Track/Core
@onready var left_line:Line2D = $Track/LeftWall
@onready var right_line:Line2D = $Track/RightWall

@export_tool_button("Save track") var save_bt: Callable = save_track
@export var track: TrackData


func _ready() -> void:
    pass

func _process(_delta: float) -> void:
    if track != null:
        track.compile_curves()
        update_lines()

func update_lines() -> void:
    core_line.set_points(track.core.get_baked_points())
    left_line.set_points(track.l_wall.get_baked_points())
    right_line.set_points(track.r_wall.get_baked_points())

func save_track() -> void:
    pass