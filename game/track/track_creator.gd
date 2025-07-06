extends Node2D


@onready var camera:Camera2D = $Camera
@onready var core_line:Line2D = $Track/Core
@onready var left_line:Line2D = $Track/LeftWall
@onready var right_line:Line2D = $Track/RightWall

@export var track_data: Array[TrackSegmentData]
var core: Curve2D
var left_wall: Curve2D
var right_wall: Curve2D
var curr_track: int = 0
var curr_width_l: float = 0.
var curr_width_r: float = 0.
var last_width_changer_track: int = 0

func _ready() -> void:
    compile_track_curves()
    update_lines()

func update_lines() -> void:
    core_line.set_points(core.get_baked_points())
    left_line.set_points(left_wall.get_baked_points())
    right_line.set_points(right_wall.get_baked_points())

func get_current_angle() -> float:
    var tangent:Vector2 = get_current_tangent()
    if tangent == Vector2.ZERO:
        return 0.
    else:
        return tangent.angle()

func get_current_tangent() -> Vector2:
    if core.point_count > 1:
        if core.get_point_in(core.point_count-1) != Vector2.ZERO:
            return -core.get_point_in(core.point_count-1).normalized()
        else:
            return (core.get_point_position(core.point_count-1)-core.get_point_position(core.point_count-2)).normalized()
    else:
        return Vector2.ZERO

func compile_track_curves() -> void:
    core = Curve2D.new()
    left_wall = Curve2D.new()
    right_wall = Curve2D.new()
    curr_width_l = 0.
    curr_width_r = 0.

    for i in track_data.size():
        var t_d:TrackSegmentData = track_data[i]
        if t_d.l_wall_dist > 0. and t_d.r_wall_dist > 0.:
            curr_width_l = t_d.l_wall_dist
            curr_width_r = t_d.r_wall_dist
        
        if i == 0:
            core.add_point(Vector2.ZERO)
            left_wall.add_point(Vector2(0., -curr_width_l))
            right_wall.add_point(Vector2(0., curr_width_r))
        
        var pos:Vector2 = core.get_point_position(core.point_count-1)
        var angle:float = get_current_angle()

        var p0_out:Vector2
        var p1:Vector2
        var p1_in:Vector2

        if t_d.l_wall_dist > 0. and t_d.r_wall_dist > 0.:
            p0_out = Vector2(t_d.length*.5, 0.).rotated(angle)
            p1 = pos + Vector2(t_d.length, 0.).rotated(angle)
            p1_in = Vector2(-t_d.length*.5, 0.).rotated(angle)
        else:
            p0_out = Vector2(abs(t_d.curvature)*t_d.length*.5, 0.)
            p0_out = p0_out.rotated(angle)
            p1 = Vector2(t_d.length*(1-abs(t_d.curvature/5.)), 0.).rotated(t_d.curvature*PI/4.)
            p1 = p1.rotated(angle) + pos
            p1_in = Vector2(-abs(t_d.curvature)*t_d.length*.5, 0.).rotated(t_d.curvature*PI/2.)
            p1_in = p1_in.rotated(angle)

        core.set_point_out(core.point_count-1, p0_out)
        core.add_point(p1, p1_in)

        var normal:Vector2 = get_current_tangent().orthogonal()
        var left_p:Vector2 = p1+normal*curr_width_l
        left_wall.set_point_out(left_wall.point_count-1, p0_out)
        left_wall.add_point(left_p, p1_in)
        var right_p:Vector2 = p1-normal*curr_width_r
        right_wall.set_point_out(right_wall.point_count-1, p0_out)
        right_wall.add_point(right_p, p1_in)