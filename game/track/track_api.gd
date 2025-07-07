@tool
extends HTTPRequest
class_name TrackAPI

signal track_saved()
signal track_loaded(track:TrackData)

var endpoint_template: String = "http://127.0.0.1:8000/tracks/%s"


func save(track: TrackData) -> void:
    request_completed.connect(_on_track_saved)
    var endpoint: String = endpoint_template % track.track_id
    print(endpoint)
    var track_json: String = JSON.stringify(track.to_dict())
    request(endpoint, [], HTTPClient.METHOD_PUT, track_json)

func load(track_id: String) -> void:
    request_completed.connect(_on_track_loaded)
    var endpoint: String = endpoint_template % track_id
    print(endpoint)
    request(endpoint)

func _on_track_saved(
        result: int,
        _response_code: int,
        _headers: PackedStringArray,
        _body: PackedByteArray,
    ) -> void:
    if result != HTTPRequest.RESULT_SUCCESS:
        push_error("Track not saved")
    print("Pista salva")
    if request_completed.is_connected(_on_track_saved):
        request_completed.disconnect(_on_track_saved)
    track_saved.emit()

func _on_track_loaded(
        result: int,
        _response_code: int,
        _headers: PackedStringArray,
        body: PackedByteArray,
    ) -> void:
    if result != HTTPRequest.RESULT_SUCCESS:
        push_error("Track not loaded")
    var track: TrackData
    var track_dict: Dictionary = JSON.parse_string(body.get_string_from_utf8())
    if track_dict != null:
        track = TrackData.from_dict(track_dict)
    if request_completed.is_connected(_on_track_loaded):
        request_completed.disconnect(_on_track_loaded)
    track_loaded.emit(track)