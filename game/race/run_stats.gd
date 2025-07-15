extends Resource
class_name RunStats

var racer: Racer
var track: Track
var progress: float = 0.
var max_progress: float = 0.
var finished: bool = false
var time_stuck: float = 0.
var progress_history: Array[float] = []
var position_history: Array[Vector2] = []


static func create(
        _racer: Racer,
        _track: Track,
    ) -> RunStats:
    
    var stats = RunStats.new()
    stats.racer = _racer
    stats.track = _track
    return stats

func to_dict() -> Dictionary:
    return {
        "racer": racer.data.racer_id,
        "track": track.data.track_id,
        "position_history": Serializer.from_list(position_history)
    }

func check_progress(delta: float) -> void:
    if not finished:
        progress = track.data.core.get_closest_offset(track.to_local(racer.global_position))
        max_progress = maxf(progress, max_progress)
        if progress >= track.data.core.get_baked_length():
            finished = true
        if progress <= max_progress:
            time_stuck += delta
        else:
            time_stuck = 0.

func record_position() -> void:
    position_history.append(racer.position)

func record_progress() -> void:
    progress_history.append(progress)

func get_progress_fraction() -> float:
    return progress / track.data.core.get_baked_length()