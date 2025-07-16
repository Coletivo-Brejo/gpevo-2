extends Node2D
class_name Run

const scene_path: String = "res://race/run.tscn"

@onready var camera: Camera2D = $Camera
@onready var stat_collection_timer: Timer = $StatCollectionTimer
@onready var begin_timer: Timer = $BeginTimer
@onready var end_timer: Timer = $EndTimer
@onready var run_timer: Timer = $RunTimer
@onready var api: API = $API

@export var run_id: String
@export var track_data: TrackData
@export var racers_data: Array[RacerData]
@export_group("Settings")
@export_range(0., 5., 1.) var begin_countdown: float = 3.
@export_range(0., 5., 1.) var end_countdown: float = 3.
@export_range(0., 10., 1.) var stuck_timeout: float = 5.
@export_range(0., 120., 10.) var run_timeout: float = 60.
@export var end_on_first_finish: bool = false
@export var follow_first: bool = true
@export var stat_collection_frequency: float = 1.
var track: Track
var racers: Array[Racer]
var stats: Array[RunStats]
var running: bool
var elapsed_time: float


static func create(
		_run_id: String,
		_track: TrackData,
		_racers: Array[RacerData],
	) -> Run:

	var run: Run = load(scene_path).instantiate()
	run.run_id = _run_id
	run.track_data = _track
	run.racers_data = _racers
	return run

func to_dict() -> Dictionary:
	var racer_ids: Array[String] = []
	for r in racers:
		racer_ids.append(r.data.racer_id)
	return {
		"run_id": run_id,
		"track_id": track.data.track_id,
		"racer_ids": racer_ids,
		"elapsed_time": elapsed_time,
		"stats": Serializer.from_list(stats),
	}

func _ready() -> void:
	running = false
	elapsed_time = 0.
	track = Track.create(track_data)
	add_child(track)
	for r in racers_data:
		var racer = Racer.create(r)
		racers.append(racer)
		add_child(racer)
		if begin_countdown > 0.:
			racer.set_paused(true)
		stats.append(RunStats.create(racer, track))
	if end_countdown > 0.:
		end_timer.set_wait_time(end_countdown)
		end_timer.timeout.connect(finish)
	if stat_collection_frequency > 0.:
		stat_collection_timer.set_wait_time(1./stat_collection_frequency)
		stat_collection_timer.timeout.connect(_on_stat_collection)
	if run_timeout > 0.:
		run_timer.set_wait_time(run_timeout)
		run_timer.timeout.connect(end_run)
	if begin_countdown > 0.:
		begin_timer.set_wait_time(begin_countdown)
		begin_timer.timeout.connect(begin_run)
		begin_timer.start()
	else:
		begin_run()

func _process(delta: float) -> void:
	if running:
		elapsed_time += delta
		var first_place: Racer = racers[0]
		var max_progress: float = stats[0].progress
		var any_finished: bool = false
		var all_finished: bool = true
		for stat in stats:
			stat.check_progress(delta)
			any_finished = any_finished or stat.finished
			all_finished = all_finished and stat.finished
			if stat.progress > max_progress:
				first_place = stat.racer
				max_progress = stat.progress
		if any_finished and end_on_first_finish:
			end_run()
		elif all_finished:
			end_run()
		if follow_first:
			camera.set_position(first_place.position)

func begin_run() -> void:
	for racer in racers:
		racer.set_paused(false)
	if stat_collection_frequency > 0.:
		stat_collection_timer.start()
	if run_timeout > 0.:
		run_timer.start()
	running = true

func end_run() -> void:
	running = false
	stat_collection_timer.stop()
	run_timer.stop()
	for stat in stats:
		stat.check_progress(0.)
		stat.record_history(elapsed_time)
	save_results()
	for racer in racers:
		racer.set_paused(true)
	if end_countdown > 0.:
		end_timer.start()
	else:
		finish()

func finish() -> void:
	get_tree().quit()

func _on_stat_collection() -> void:
	for stat in stats:
		stat.record_history(elapsed_time)

func save_results() -> void:
	api.save_from_dict("/runs", run_id, to_dict())
