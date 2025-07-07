@tool
extends Resource
class_name TrackSegmentData

@export_range(0., 1000., 50.) var length: float:
    set(value): length = value; emit_changed()
@export_range(-1., 1., .1) var curvature: float:
    set(value): curvature = value; emit_changed()
@export_range(0., 200., 10.) var l_wall_dist: float:
    set(value): l_wall_dist = value; emit_changed()
@export_range(0., 2., .05) var l_wall_curv: float:
    set(value): l_wall_curv = value; emit_changed()
@export_range(0., 200., 10.) var r_wall_dist: float:
    set(value): r_wall_dist = value; emit_changed()
@export_range(0., 2., .05) var r_wall_curv: float:
    set(value): r_wall_curv = value; emit_changed()


static func create(
        _length: float = 0.,
        _curvature: float = 0.,
        _l_wall_dist: float = 0.,
        _l_wall_curv: float = 1.,
        _r_wall_dist: float = 0.,
        _r_wall_curv: float = 1.,
    ) -> TrackSegmentData:
    
    var segment = TrackSegmentData.new()
    segment.length = _length
    segment.curvature = _curvature
    segment.l_wall_dist = _l_wall_dist
    segment.l_wall_curv = _l_wall_curv
    segment.r_wall_dist = _r_wall_dist
    segment.r_wall_curv = _r_wall_curv
    return segment

static func from_dict(dict: Dictionary) -> TrackSegmentData:
    var segment = TrackSegmentData.create(
        dict["length"],
        dict["curvature"],
        dict["l_wall_dist"],
        dict["l_wall_curv"],
        dict["r_wall_dist"],
        dict["r_wall_curv"],
    )
    return segment

func to_dict() -> Dictionary:
    return {
        "length": length,
        "curvature": curvature,
        "l_wall_dist": l_wall_dist,
        "l_wall_curv": l_wall_curv,
        "r_wall_dist": r_wall_dist,
        "r_wall_curv": r_wall_curv,
    }
