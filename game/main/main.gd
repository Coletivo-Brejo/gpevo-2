extends Node2D

@onready var api: API = $API


func _ready() -> void:
    var url_params: Dictionary = URLReader.read_params()
    # var url_params: Dictionary = {"mode": "training", "training_id": "training_7"}
    var mode: String = url_params.get("mode")
    if mode != null:
        if mode == "training":
            var training_id: String = url_params.get("training_id")
            if training_id != null:
                load_training(training_id)

func load_training(training_id: String) -> void:
    api.resource_loaded.connect(_on_training_loaded)
    api.load("/trainings", training_id)

func _on_training_loaded(training_dict: Dictionary) -> void:
    api.resource_loaded.disconnect(_on_training_loaded)
    if training_dict != null:
        var training_data = TrainingData.from_dict(training_dict)
        var training = Training.create(training_data)
        add_child(training)
