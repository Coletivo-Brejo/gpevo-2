extends Resource
class_name RunData

@export var run_id: String
@export var track_data: TrackData
@export var racers_data: Array[RacerData]
@export var setup: RunSetup
var elapsed_time: float
var end_reason: String
var stats: Array[RunStats]

var finished: bool = false


static func create(
		_run_id: String,
		_track_data: TrackData,
		_racers_data: Array[RacerData],
		_setup: RunSetup,
	) -> RunData:

	var run = RunData.new()
	run.run_id = _run_id
	run.track_data = _track_data
	run.racers_data = _racers_data
	run.setup = _setup
	return run

static func from_dict(dict: Dictionary) -> RunData:
	var _racers_data: Array[RacerData] = []
	for r in dict["racers_data"]:
		_racers_data.append(RacerData.from_dict(r))

	var run = RunData.create(
		dict["run_id"],
		TrackData.from_dict(dict["track_data"]),
		_racers_data,
		RunSetup.from_dict(dict["setup"]),
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
		"setup": setup.to_dict(),
		"elapsed_time": elapsed_time,
		"end_reason": end_reason,
		"stats": Serializer.from_list(stats)
	}

func clone() -> RunData:
	var dict: Dictionary = to_dict()
	dict["racers_data"] = []
	for r in racers_data:
		dict["racers_data"].append(r.to_dict())
	dict["track_data"] = track_data.to_dict()
	return from_dict(dict)

func get_racer_stats(racer_id: String) -> RunStats:
	for s in stats:
		if s.racer_data.racer_id == racer_id:
			return s
	return null