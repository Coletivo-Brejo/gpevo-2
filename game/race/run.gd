extends Node2D
class_name Run

const scene_path: String = "res://race/run.tscn"

@onready var camera: Camera2D = $Camera
@onready var stat_collection_timer: Timer = $StatCollectionTimer
@onready var begin_timer: Timer = $BeginTimer
@onready var end_timer: Timer = $EndTimer

@export var track_data: TrackData
@export var racers_data: Array[RacerData]
@export_group("Settings")
@export_range(0., 5., 1.) var begin_countdown: float = 3.
@export_range(0., 5., 1.) var end_countdown: float = 3.
@export_range(0., 10., 1.) var stuck_timeout: float = 5.
@export var end_on_first_finish: bool = false
@export var follow_first: bool = true
@export var stat_collection_frequency: float = 1.
var track: Track
var racers: Array[Racer]
var stats: Array[RunStats]


static func create(
        _track: TrackData,
        _racers: Array[RacerData],
    ) -> Run:
    
    var run: Run = load(scene_path).instantiate()
    run.track_data = _track
    run.racers_data = _racers
    return run

func _ready() -> void:
    track = Track.create(track_data)
    add_child(track)
    for r in racers_data:
        var racer = Racer.create(r)
        if begin_countdown > 0.:
            racer.set_paused(true)
        racers.append(racer)
        add_child(racer)
        stats.append(RunStats.create(racer, track))
    if begin_countdown > 0.:
        begin_timer.set_wait_time(begin_countdown)
        begin_timer.timeout.connect(begin_run)
        begin_timer.start()
    if end_countdown > 0.:
        end_timer.set_wait_time(end_countdown)
        end_timer.timeout.connect(end_run)
    if stat_collection_frequency > 0.:
        stat_collection_timer.set_wait_time(1./stat_collection_frequency)
        stat_collection_timer.timeout.connect(_on_stat_collection)

func _process(delta: float) -> void:
    for stat in stats:
        stat.check_progress(delta)

func begin_run() -> void:
    for racer in racers:
        racer.set_paused(false)
    if stat_collection_frequency > 0.:
        stat_collection_timer.start()

func end_run() -> void:
    for racer in racers:
        racer.set_paused(true)
    stat_collection_timer.stop()

func _on_stat_collection() -> void:
    for stat in stats:
        stat.record_position()
        stat.record_progress()