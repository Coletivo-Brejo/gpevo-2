@tool
extends HTTPRequest
class_name API

signal resource_saved()
signal resource_loaded(resource_dict: Dictionary)
signal post_responded(body: Variant)
signal put_responded(body: Variant)

@export var url: String = "http://127.0.0.1:8000"


func save(route: String, resource_id: String, resource: Resource) -> void:
	if resource.has_method("to_dict"):
		var resource_dict: Dictionary = resource.to_dict()
		save_from_dict(route, resource_id, resource_dict)
	else:
		print("Recurso não pode ser serializado")

func save_from_dict(route: String, resource_id: String, resource_dict: Dictionary) -> void:
	disconnect_all()
	request_completed.connect(_on_resource_saved)
	var endpoint: String = "%s%s/%s" % [url, route, resource_id]
	print(endpoint)
	var resource_json: String = JSON.stringify(resource_dict)
	request(endpoint, [], HTTPClient.METHOD_PUT, resource_json)

func load(route: String, resource_id: String) -> void:
	disconnect_all()
	request_completed.connect(_on_resource_loaded)
	var endpoint: String = "%s%s/%s" % [url, route, resource_id]
	print(endpoint)
	request(endpoint)

func post(route: String, body: Variant) -> void:
	disconnect_all()
	request_completed.connect(_on_post_responded)
	var endpoint: String = "%s%s" % [url, route]
	var body_json: String = JSON.stringify(body)
	request(endpoint, [], HTTPClient.METHOD_POST, body_json)

func put(route: String, body: Variant) -> void:
	disconnect_all()
	request_completed.connect(_on_put_responded)
	var endpoint: String = "%s%s" % [url, route]
	var body_json: String = JSON.stringify(body)
	request(endpoint, [], HTTPClient.METHOD_PUT, body_json)

func disconnect_all() -> void:
	if request_completed.is_connected(_on_resource_saved):
		request_completed.disconnect(_on_resource_saved)
	if request_completed.is_connected(_on_resource_loaded):
		request_completed.disconnect(_on_resource_loaded)
	if request_completed.is_connected(_on_post_responded):
		request_completed.disconnect(_on_post_responded)
	if request_completed.is_connected(_on_put_responded):
		request_completed.disconnect(_on_put_responded)

func _on_resource_saved(
		result: int,
		_response_code: int,
		_headers: PackedStringArray,
		_body: PackedByteArray,
	) -> void:
	if result != HTTPRequest.RESULT_SUCCESS:
		push_error("Falha ao salvar recurso")
	# print(_body.get_string_from_utf8())
	print("Recurso salvo")
	disconnect_all()
	resource_saved.emit()

func _on_resource_loaded(
		result: int,
		_response_code: int,
		_headers: PackedStringArray,
		body: PackedByteArray,
	) -> void:
	if result != HTTPRequest.RESULT_SUCCESS:
		push_error("Falha ao carregar recurso")
	var resource_dict: Dictionary = JSON.parse_string(body.get_string_from_utf8())
	if resource_dict != null:
		disconnect_all()
		resource_loaded.emit(resource_dict)

func _on_post_responded(
		result: int,
		_response_code: int,
		_headers: PackedStringArray,
		body: PackedByteArray,
	) -> void:
	if result != HTTPRequest.RESULT_SUCCESS:
		push_error("Falha ao carregar recurso")
	var parsed_body: Variant = JSON.parse_string(body.get_string_from_utf8())
	# print(parsed_body)
	if parsed_body != null:
		disconnect_all()
		post_responded.emit(parsed_body)

func _on_put_responded(
		result: int,
		_response_code: int,
		_headers: PackedStringArray,
		body: PackedByteArray,
	) -> void:
	if result != HTTPRequest.RESULT_SUCCESS:
		push_error("Falha ao carregar recurso")
	var parsed_body: Variant = JSON.parse_string(body.get_string_from_utf8())
	# print(parsed_body)
	if parsed_body != null:
		disconnect_all()
		put_responded.emit(parsed_body)
