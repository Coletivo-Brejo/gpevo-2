@tool
extends Node2D
class_name MaskedCapsule

@onready var texture_sprite: Sprite2D = find_child("TextureSprite")

@export var texture: Texture2D:
    set(value):
        texture = value
        if texture_sprite != null:
            texture_sprite.set_texture(texture)