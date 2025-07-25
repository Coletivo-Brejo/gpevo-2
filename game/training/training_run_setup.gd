extends Resource
class_name TrainingRunSetup

@export var track_id: String
@export var run_setup: RunSetup


static func create(
        _track_id: String,
        _run_setup: RunSetup,
    ) -> TrainingRunSetup:

    var setup = TrainingRunSetup.new()
    setup.track_id = _track_id
    setup.run_setup = _run_setup
    return setup

static func from_dict(dict: Dictionary) -> TrainingRunSetup:
    var setup = TrainingRunSetup.create(
        dict["track_id"],
        RunSetup.from_dict(dict["run_setup"]),
    )
    return setup

func to_dict() -> Dictionary:
    return {
        "track_id": track_id,
        "run_setup": run_setup.to_dict(),
    }