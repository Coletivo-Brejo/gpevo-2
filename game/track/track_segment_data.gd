extends Resource
class_name TrackSegmentData

@export var length: float
@export var curvature: float
@export var l_wall_dist: float
@export var l_wall_curv: float
@export var r_wall_dist: float
@export var r_wall_curv: float


static func create(
        _length: float = 0.,
        _curvature: float = 0.,
        _l_wall_dist: float = 0.,
        _l_wall_curv: float = 0.,
        _r_wall_dist: float = 0.,
        _r_wall_curv: float = 0.,
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
