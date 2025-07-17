extends Resource
class_name RunStats

signal racer_finished()
signal racer_stuck()

var racer: Racer
var track: Track
var lap: int = 0
var progress: float = 0.
var max_progress: float = 0.
var finished: bool = false
var stuck: bool = false
var time_stuck: float = 0.
var time_history: Array[float] = []
var progress_history: Array[float] = []
var position_history: Array[Vector2] = []
var stuck_timeout: float
var laps: int
var checkpoint: int = 0
var track_length: float = 0.


static func create(
        _racer: Racer,
        _track: Track,
        _stuck_timeout: float = 0.,
        _laps: int = 1,
    ) -> RunStats:
    
    var stats = RunStats.new()
    stats.racer = _racer
    stats.track = _track
    stats.stuck_timeout = _stuck_timeout
    stats.laps = _laps
    stats.track_length = _track.data.core.get_baked_length()
    return stats

func to_dict() -> Dictionary:
    return {
        "racer_id": racer.data.racer_id,
        "track_id": track.data.track_id,
        "lap": lap,
        "max_progress": max_progress,
        "finished": finished,
        "stuck": stuck,
        "time_history": time_history,
        "progress_history": progress_history,
        "position_history": Serializer.from_list(position_history)
    }

func check_progress(delta: float) -> void:
    if not finished and not stuck and not racer.paused:
        var lap_progress: float = track.data.core.get_closest_offset(track.to_local(racer.global_position))
        if assert_lap_progress(lap_progress):
            var new_checkpoint: int = floori(lap_progress / track.data.core.get_baked_length() * 10) % 10
            if checkpoint == 9 and new_checkpoint == 0:
                lap += 1
            checkpoint = new_checkpoint
            progress = lap*track_length + lap_progress
            if lap >= laps:
                finished = true
                racer_finished.emit()
            if progress <= max_progress:
                update_stuck_time(delta)
            else:
                time_stuck = 0.
                max_progress = progress
        else:
            update_stuck_time(delta)

func assert_lap_progress(lap_progress: float) -> bool:
    var ratio: float = lap_progress / track_length
    var _checkpoint: int = floori(ratio*10) % 10
    if _checkpoint == checkpoint:
        return true
    elif _checkpoint == (checkpoint+1) % 10:
        return true
    else:
        return false

func update_stuck_time(delta: float) -> void:
    time_stuck += delta
    if stuck_timeout > 0. and time_stuck > stuck_timeout:
        stuck = true
        racer_stuck.emit()

func record_history(time: float) -> void:
    print("Lap: %d" % lap)
    print("Checkpoint: %d" % checkpoint)
    if not finished and not stuck and not racer.paused:
        time_history.append(time)
        progress_history.append(max_progress)
        position_history.append(racer.position)

func get_progress_fraction() -> float:
    return progress / track.data.core.get_baked_length()