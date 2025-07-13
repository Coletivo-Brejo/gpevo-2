extends CharacterBody2D

@export var speed: float = 400.



func _draw() -> void:
    draw_circle(Vector2.ZERO, 10., Color.WHITE)

func _physics_process(_delta: float) -> void:
    get_input()
    move_and_slide()

func get_input() -> void:
    var input_direction: Vector2 = Input.get_vector("left", "right", "up", "down")
    velocity = input_direction * speed