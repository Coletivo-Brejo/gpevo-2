extends Node2D
class_name Run

signal run_ended()
signal run_finished()

const scene_path: String = "res://race/run.tscn"

@onready var camera: Camera2D = $Camera
@onready var stat_collection_timer: Timer = $StatCollectionTimer
@onready var begin_timer: Timer = $BeginTimer
@onready var end_timer: Timer = $EndTimer
@onready var run_timer: Timer = $RunTimer
@onready var api: API = $API

@export var data: RunData
@export var follow_first: bool = true
var track: Track
var racers: Array[Racer]
var stats: Array[RunStats]
var running: bool


static func create(
		_data: RunData,
		_follow_first: bool,
	) -> Run:

	var run: Run = load(scene_path).instantiate()
	run.data = _data
	run.follow_first = _follow_first
	return run

func _ready() -> void:
	data.elapsed_time = 0.
	running = false
	track = Track.create(data.track_data)
	if data.mirrored:
		track.set_scale(Vector2(-1., 1.))
	add_child(track)
	for r in data.racers_data:
		var racer = Racer.create(r)
		racers.append(racer)
		add_child(racer)
		if data.begin_countdown > 0.:
			racer.set_paused(true)
		var stat = RunStats.create(
			racer,
			track,
			data.stuck_timeout,
			data.laps,
		)
		stats.append(stat)
		data.stats.append(stat)
		stat.racer_finished.connect(_on_racer_finished.bind(racer, stat))
		stat.racer_stuck.connect(_on_racer_stuck.bind(racer, stat))
	if data.end_countdown > 0.:
		end_timer.set_wait_time(data.end_countdown)
		end_timer.timeout.connect(finish)
	if data.stat_collection_frequency > 0.:
		stat_collection_timer.set_wait_time(1./data.stat_collection_frequency)
		stat_collection_timer.timeout.connect(_on_stat_collection)
	if data.run_timeout > 0.:
		run_timer.set_wait_time(data.run_timeout)
		run_timer.timeout.connect(end_run.bind("timeout"))
	if data.begin_countdown > 0.:
		begin_timer.set_wait_time(data.begin_countdown)
		begin_timer.timeout.connect(begin_run)
		begin_timer.start()
	else:
		begin_run()

func _process(delta: float) -> void:
	if running:
		data.elapsed_time += delta
		var first_place: Racer = racers[0]
		var max_progress: float = stats[0].progress
		var any_finished: bool = false
		var all_finished: bool = true
		var all_stuck: bool = true
		var all_finished_or_stuck: bool = true
		for stat in stats:
			stat.check_progress(delta)
			any_finished = any_finished or stat.finished
			all_finished = all_finished and stat.finished
			all_stuck = all_stuck and stat.stuck
			all_finished_or_stuck = all_finished_or_stuck and (stat.finished or stat.stuck)
			if stat.progress > max_progress:
				first_place = stat.racer
				max_progress = stat.progress
		if any_finished and data.end_on_first_finish:
			end_run("first finished")
		elif all_finished:
			end_run("all finished")
		elif all_stuck:
			end_run("all stuck")
		elif all_finished_or_stuck:
			end_run("all finished or stuck")
		if follow_first:
			camera.set_position(first_place.position)

func begin_run() -> void:
	for racer in racers:
		racer.set_paused(false)
	if data.stat_collection_frequency > 0.:
		stat_collection_timer.start()
	if data.run_timeout > 0.:
		run_timer.start()
	running = true

func end_run(reason: String) -> void:
	data.end_reason = reason
	running = false
	stat_collection_timer.stop()
	run_timer.stop()
	for stat in stats:
		stat.record_history(data.elapsed_time)
	for racer in racers:
		racer.set_paused(true)
	run_ended.emit()
	if data.end_countdown > 0.:
		end_timer.start()
	else:
		finish()

func finish() -> void:
	run_finished.emit()

func _on_stat_collection() -> void:
	for stat in stats:
		stat.record_history(data.elapsed_time)

func _on_racer_finished(racer: Racer, stat: RunStats) -> void:
	stat.record_history(data.elapsed_time)
	racer.set_paused(true)

func _on_racer_stuck(racer: Racer, stat: RunStats) -> void:
	stat.record_history(data.elapsed_time)
	racer.set_paused(true)

func save() -> void:
	api.save("/runs", data.run_id, data)
