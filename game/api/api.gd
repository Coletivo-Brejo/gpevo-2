@tool
extends HTTPRequest
class_name API

signal resource_saved()
signal resource_loaded(resource_dict: Dictionary)

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

func disconnect_all() -> void:
	if request_completed.is_connected(_on_resource_saved):
		request_completed.disconnect(_on_resource_saved)
	if request_completed.is_connected(_on_resource_loaded):
		request_completed.disconnect(_on_resource_loaded)

func _on_resource_saved(
		result: int,
		_response_code: int,
		_headers: PackedStringArray,
		_body: PackedByteArray,
	) -> void:
	if result != HTTPRequest.RESULT_SUCCESS:
		push_error("Falha ao salvar recurso")
	print(_body.get_string_from_utf8())
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
