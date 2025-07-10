@tool
extends HTTPRequest
class_name ShipAPI

signal ship_saved()
signal ship_loaded(ship:ShipData)

var endpoint_template: String = "http://127.0.0.1:8000/ships/%s"


func save(ship: ShipData) -> void:
    request_completed.connect(_on_ship_saved)
    var endpoint: String = endpoint_template % ship.ship_id
    print(endpoint)
    var ship_json: String = JSON.stringify(ship.to_dict())
    print(ship_json)
    request(endpoint, [], HTTPClient.METHOD_PUT, ship_json)

func load(ship_id: String) -> void:
    request_completed.connect(_on_ship_loaded)
    var endpoint: String = endpoint_template % ship_id
    print(endpoint)
    request(endpoint)

func _on_ship_saved(
        result: int,
        _response_code: int,
        _headers: PackedStringArray,
        _body: PackedByteArray,
    ) -> void:
    if result != HTTPRequest.RESULT_SUCCESS:
        push_error("Ship not saved")
    print("Ship saved")
    if request_completed.is_connected(_on_ship_saved):
        request_completed.disconnect(_on_ship_saved)
    ship_saved.emit()

func _on_ship_loaded(
        result: int,
        _response_code: int,
        _headers: PackedStringArray,
        body: PackedByteArray,
    ) -> void:
    if result != HTTPRequest.RESULT_SUCCESS:
        push_error("Ship not loaded")
    var ship: ShipData
    var ship_dict: Dictionary = JSON.parse_string(body.get_string_from_utf8())
    if ship_dict != null:
        ship = ShipData.from_dict(ship_dict)
    if request_completed.is_connected(_on_ship_loaded):
        request_completed.disconnect(_on_ship_loaded)
    ship_loaded.emit(ship)