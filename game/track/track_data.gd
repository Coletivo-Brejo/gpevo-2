@tool
extends Resource
class_name TrackData

@export var track_id: String
@export var name: String
@export var segments: Array[TrackSegmentData]
var core: Curve2D
var l_wall: Curve2D
var r_wall: Curve2D
var length: float


static func create(
        _track_id: String = "",
        _name: String = "",
        _segments: Array[TrackSegmentData] = [],
    ) -> TrackData:
    var track = TrackData.new()
    track.track_id = _track_id
    track.name = _name
    track.segments = _segments
    track.compile_curves()
    return track

static func from_dict(dict: Dictionary) -> TrackData:
    var _segments: Array[TrackSegmentData] = []
    for s in dict["segments"]:
        _segments.append(TrackSegmentData.from_dict(s))
    var track = TrackData.create(
        dict["track_id"],
        dict["name"],
        _segments,
    )
    return track

func to_dict() -> Dictionary:
    return {
        "track_id": track_id,
        "name": name,
        "segments": Serializer.from_list(segments),
        "core": Serializer.from_list(core.get_baked_points()),
        "l_wall": Serializer.from_list(l_wall.get_baked_points()),
        "r_wall": Serializer.from_list(r_wall.get_baked_points()),
        "length": length,
    }

func get_current_tangent() -> Vector2:
    if core.point_count > 1:
        if core.get_point_in(core.point_count-1) != Vector2.ZERO:
            return -core.get_point_in(core.point_count-1).normalized()
        else:
            return (core.get_point_position(core.point_count-1)-core.get_point_position(core.point_count-2)).normalized()
    else:
        return Vector2.ZERO

func get_current_angle() -> float:
    var tangent:Vector2 = get_current_tangent()
    if tangent == Vector2.ZERO:
        return 0.
    else:
        return tangent.angle()+PI/2.

func compile_curves() -> void:
    core = Curve2D.new()
    l_wall = Curve2D.new()
    r_wall = Curve2D.new()
    var curr_width_l: float = 0.
    var curr_width_r: float = 0.

    for i in segments.size():
        var s:TrackSegmentData = segments[i]
        if s == null:
            continue

        if s.l_wall_dist > 0. and s.r_wall_dist > 0.:
            curr_width_l = s.l_wall_dist
            curr_width_r = s.r_wall_dist
        
        if i == 0:
            core.add_point(Vector2.ZERO)
            l_wall.add_point(Vector2.LEFT*curr_width_l)
            r_wall.add_point(Vector2.RIGHT*curr_width_r)
        
        var pos:Vector2 = core.get_point_position(core.point_count-1)
        var angle:float = get_current_angle()

        var p0_out:Vector2
        var p1:Vector2
        var p1_in:Vector2

        if s.l_wall_dist > 0. and s.r_wall_dist > 0.:
            p0_out = (Vector2.UP*s.length*.5).rotated(angle)
            p1 = pos + (Vector2.UP*s.length).rotated(angle)
            p1_in = (Vector2.DOWN*s.length*.5).rotated(angle)
        else:
            p0_out = (Vector2.UP*abs(s.curvature)*s.length*.5)
            p0_out = p0_out.rotated(angle)
            p1 = (Vector2.UP*s.length*(1-abs(s.curvature/5.))).rotated(s.curvature*PI/4.)
            p1 = p1.rotated(angle) + pos
            p1_in = (Vector2.DOWN*abs(s.curvature)*s.length*.5).rotated(s.curvature*PI/2.)
            p1_in = p1_in.rotated(angle)

        core.set_point_out(core.point_count-1, p0_out)
        core.add_point(p1, p1_in)

        var normal:Vector2 = get_current_tangent().orthogonal()
        var left_p:Vector2 = p1+normal*curr_width_l
        l_wall.set_point_out(l_wall.point_count-1, p0_out*s.l_wall_curv)
        l_wall.add_point(left_p, p1_in*s.l_wall_curv)
        var right_p:Vector2 = p1-normal*curr_width_r
        r_wall.set_point_out(r_wall.point_count-1, p0_out*s.r_wall_curv)
        r_wall.add_point(right_p, p1_in*s.r_wall_curv)

        length = core.get_baked_length()