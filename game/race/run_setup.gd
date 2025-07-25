extends Resource
class_name RunSetup

@export_range(0., 5., 1.) var begin_countdown: float = 3.
@export_range(0., 5., 1.) var end_countdown: float = 3.
@export_range(0., 10., 1.) var stuck_timeout: float = 5.
@export_range(0., 120., 10.) var run_timeout: float = 60.
@export var follow_first: bool = true
@export var end_on_first_finish: bool = false
@export var stat_collection_frequency: float = 1.
@export var mirrored: bool = false
@export var laps: int = 1


static func create(
        _begin_countdown: float,
        _end_countdown: float,
        _stuck_timeout: float,
        _run_timeout: float,
        _follow_first: bool,
        _end_on_first_finish: bool,
        _stat_collection_frequency: float,
        _mirrored: bool = false,
        _laps: int = 1,
    ) -> RunSetup:

    var run = RunSetup.new()
    run.begin_countdown = _begin_countdown
    run.end_countdown = _end_countdown
    run.stuck_timeout = _stuck_timeout
    run.run_timeout = _run_timeout
    run.follow_first = _follow_first
    run.end_on_first_finish = _end_on_first_finish
    run.stat_collection_frequency = _stat_collection_frequency
    run.mirrored = _mirrored
    run.laps = _laps
    return run

static func from_dict(dict: Dictionary) -> RunSetup:
    var run = RunSetup.create(
        dict["begin_countdown"],
        dict["end_countdown"],
        dict["stuck_timeout"],
        dict["run_timeout"],
        dict["follow_first"],
        dict["end_on_first_finish"],
        dict["stat_collection_frequency"],
        dict["mirrored"],
        dict["laps"],
    )
    return run

func to_dict() -> Dictionary:
    return {
        "begin_countdown": begin_countdown,
        "end_countdown": end_countdown,
        "stuck_timeout": stuck_timeout,
        "run_timeout": run_timeout,
        "follow_first": follow_first,
        "end_on_first_finish": end_on_first_finish,
        "stat_collection_frequency": stat_collection_frequency,
        "mirrored": mirrored,
        "laps": laps,
    }