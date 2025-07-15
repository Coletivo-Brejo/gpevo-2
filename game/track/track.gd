extends StaticBody2D
class_name Track

const scene_path: String = "res://track/track.tscn"

@onready var core: Line2D = $Core
@onready var l_wall: Line2D = $LeftWall
@onready var r_wall: Line2D = $RightWall

@export var data: TrackData


static func create(
		_data: TrackData,
	) -> Track:
	var track: Track = load(scene_path).instantiate()
	track.data = _data
	return track

func _ready() -> void:
	data.compile_curves()
	create_walls()

func create_walls() -> void:
	l_wall.set_points(data.l_wall.get_baked_points())
	for i in l_wall.get_point_count()-1:
		create_segment_collider(l_wall.points[i], l_wall.points[i+1])
	r_wall.set_points(data.r_wall.get_baked_points())
	for i in r_wall.get_point_count()-1:
		create_segment_collider(r_wall.points[i], r_wall.points[i+1])

func create_segment_collider(a: Vector2, b: Vector2) -> void:
	var collider = CollisionShape2D.new()
	var segment = SegmentShape2D.new()
	segment.set_a(a)
	segment.set_b(b)
	collider.set_shape(segment)
	add_child(collider)
