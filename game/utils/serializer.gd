extends Object
class_name Serializer


static func from_color(color:Color) -> Dictionary[String, float]:
	return {"r":color.r, "g":color.g, "b":color.b, "a":color.a}

static func to_color(dict:Dictionary) -> Color:
	return Color(dict["r"], dict["g"], dict["b"], dict["a"])

static func from_packed_v2(array: PackedVector2Array) -> Array[Dictionary]:
	var dict_array: Array[Dictionary] = []
	for v in array:
		dict_array.append(from_vector2(v))
	return dict_array

static func to_packed_v2(array: Array) -> PackedVector2Array:
	var vec_array: PackedVector2Array = []
	for v_dict in array:
		vec_array.append(to_vector2(v_dict))
	return vec_array

static func from_rect(rect:Rect2) -> Dictionary[String, float]:
	return {"x":rect.position.x, "y":rect.position.y, "w":rect.size.x, "h":rect.size.y}

static func to_rect(dict:Dictionary) -> Rect2:
	return Rect2(Vector2(dict["x"], dict["y"]), Vector2(dict["w"], dict["h"]))

static func from_texture(texture:Texture2D) -> String:
	return texture.resource_path

static func to_texture(path:String) -> Texture2D:
	return load(path)

static func from_vector2(vec:Vector2) -> Dictionary[String, float]:
	return {"x":vec.x, "y":vec.y}

static func to_vector2(dict:Dictionary) -> Vector2:
	return Vector2(dict["x"], dict["y"])

static func from_vector3(vec:Vector3) -> Dictionary[String, float]:
	return {"x":vec.x, "y":vec.y, "z":vec.z}

static func to_vector3(dict:Dictionary) -> Vector3:
	return Vector3(dict["x"], dict["y"], dict["z"])

static func from_list(list:Array) -> Array[Dictionary]:
	var serialized_list:Array[Dictionary] = []
	for o in list:
		if o is Color:
			serialized_list.append(from_color(o))
		elif o is Rect2:
			serialized_list.append(from_rect(o))
		elif o is Texture2D:
			serialized_list.append(from_texture(o))
		elif o is Vector2:
			serialized_list.append(from_vector2(o))
		elif o is Vector3:
			serialized_list.append(from_vector3(o))
		elif o.has_method("to_dict"):
			serialized_list.append(o.to_dict())
	return serialized_list
