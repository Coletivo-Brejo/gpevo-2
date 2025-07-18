extends Resource
class_name RunData

@export var run_id: String
@export var track_data: TrackData
@export var racers_data: Array[RacerData]
@export_range(0., 5., 1.) var begin_countdown: float = 3.
@export_range(0., 5., 1.) var end_countdown: float = 3.
@export_range(0., 10., 1.) var stuck_timeout: float = 5.
@export_range(0., 120., 10.) var run_timeout: float = 60.
@export var end_on_first_finish: bool = false
@export var stat_collection_frequency: float = 1.
@export var mirrored: bool = false
@export var laps: int = 1
var elapsed_time: float
var end_reason: String
var stats: Array[RunStats]


static func create(
        _run_id: String,
        _track_data: TrackData,
        _racers_data: Array[RacerData],
        _begin_countdown: float,
        _end_countdown: float,
        _stuck_timeout: float,
        _run_timeout: float,
        _end_on_first_finish: bool,
        _stat_collection_frequency: float,
        _mirrored: bool = false,
        _laps: int = 1,
    ) -> RunData:

    var run = RunData.new()
    run.run_id = _run_id
    run.track_data = _track_data
    run.racers_data = _racers_data
    run.begin_countdown = _begin_countdown
    run.end_countdown = _end_countdown
    run.stuck_timeout = _stuck_timeout
    run.run_timeout = _run_timeout
    run.end_on_first_finish = _end_on_first_finish
    run.stat_collection_frequency = _stat_collection_frequency
    run.mirrored = _mirrored
    run.laps = _laps
    return run

static func from_dict(dict: Dictionary) -> RunData:
    var _racers_data: Array[RacerData] = []
    for r in dict["racers_data"]:
        _racers_data.append(RacerData.from_dict(r))

    var run = RunData.create(
        dict["run_id"],
        TrackData.from_dict(dict["track_data"]),
        _racers_data,
        dict["begin_countdown"],
        dict["end_countdown"],
        dict["stuck_timeout"],
        dict["run_timeout"],
        dict["end_on_first_finish"],
        dict["stat_collection_frequency"],
        dict["mirrored"],
        dict["laps"],
    )
    return run

func to_dict() -> Dictionary:
    var _racer_ids: Array[String] = []
    for r in racers_data:
        _racer_ids.append(r.racer_id)
    return {
        "run_id": run_id,
        "track_id": track_data.track_id,
        "racer_ids": _racer_ids,
        "begin_countdown": begin_countdown,
        "end_countdown": end_countdown,
        "stuck_timeout": stuck_timeout,
        "run_timeout": run_timeout,
        "end_on_first_finish": end_on_first_finish,
        "stat_collection_frequency": stat_collection_frequency,
        "mirrored": mirrored,
        "laps": laps,
        "elapsed_time": elapsed_time,
        "end_reason": end_reason,
        "stats": Serializer.from_list(stats)
    }