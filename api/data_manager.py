from fastapi.responses import JSONResponse
import os

from models.brain import Brain
from models.racer import Racer
from models.training import Training, TrainingEntry, TrainingInfo
from utils import get_all_resources, get_resource, now, update_resource


RACERS_PATH = "{data_path}/racers".format(
    data_path = os.environ.get("DATA_PATH")
)
RUNS_PATH = "{data_path}/runs".format(
    data_path = os.environ.get("DATA_PATH")
)
TRACKS_PATH = "{data_path}/tracks".format(
    data_path = os.environ.get("DATA_PATH")
)
TRAININGS_PATH = "{data_path}/trainings".format(
    data_path = os.environ.get("DATA_PATH")
)
TRAINING_ENTRIES_PATH = f"{TRAININGS_PATH}/entries"

def get_training_info(
        training_id: str,
    ) -> TrainingInfo|None:
    entry_dict: dict|None = get_resource(TRAINING_ENTRIES_PATH, training_id)
    if entry_dict is not None:
        training_dict: dict|None = get_resource(TRAININGS_PATH, training_id)
        if training_dict is not None:
            racer_dict: dict|None = get_resource(
                RACERS_PATH,
                training_dict["setup"]["racer_id"],
                ["racer_id", "name"],
            )
            track_dict: dict|None = get_resource(
                TRACKS_PATH,
                training_dict["setup"]["setups"][0]["track_id"],
                ["track_id", "name", "length"],
            )
            last_progress: float|None = None
            if len(training_dict["run_id_history"]) > 0:
                last_run_ids: list[str] = training_dict["run_id_history"][-1]
                last_clone_id: str = training_dict["clone_history"][-1]
                for run_id in last_run_ids:
                    run_dict: dict|None = get_resource(RUNS_PATH, run_id)
                    if run_dict is not None:
                        for stat in run_dict["stats"]:
                            if stat["racer_id"] == last_clone_id:
                                if last_progress is None:
                                    last_progress = stat["max_progress"]
                                else:
                                    last_progress = min(last_progress, stat["max_progress"])
                                break
            else:
                last_progress = 0.
            if racer_dict is not None and track_dict is not None and last_progress is not None:
                laps: int = training_dict["setup"]["setups"][0]["run_setup"]["laps"]
                final_progress: float = last_progress / track_dict["length"] / float(laps)
                info: TrainingInfo = TrainingInfo(
                    training_id = training_id,
                    entry = TrainingEntry(**entry_dict),
                    racer_id = racer_dict["racer_id"],
                    racer_name = racer_dict["name"],
                    track_id = track_dict["track_id"],
                    track_name = track_dict["name"],
                    iteration = training_dict["iteration"],
                    n_iterations = training_dict["setup"]["n_iterations"],
                    laps = laps,
                    final_progress = final_progress,
                )
                return info
    return None

def get_training_info_with_filters(
        racer_ids: list[str] = [],
        track_ids: list[str] = [],
    ) -> list[TrainingInfo]:
    info_list: list[TrainingInfo] = []
    all_entries: list[dict] = get_all_resources(TRAINING_ENTRIES_PATH)
    for e_dict in all_entries:
        info: TrainingInfo|None = get_training_info(e_dict["training_id"])
        if info is not None:
            if racer_ids is not None and len(racer_ids) > 0 and info.racer_id not in racer_ids:
                continue
            if track_ids is not None and len(track_ids) > 0 and info.track_id not in track_ids:
                continue
            info_list.append(info)
    info_list.sort(key = lambda info: info.entry.created_at, reverse = True)
    return info_list

def update_brain(racer_id: str, brain: Brain) -> JSONResponse:
    racer_dict: dict|None = get_resource(RACERS_PATH, racer_id)
    if racer_dict is not None:
        racer: Racer = Racer(**racer_dict)
        racer.brain = brain
        if racer.brain_version is None:
            racer.brain_version = 1
        else:
            racer.brain_version += 1
        return update_resource(RACERS_PATH, racer_id, racer)
    else:
        return JSONResponse({"Erro": "Corredor não encontrado"}, 404)

def update_training(training: Training) -> JSONResponse:
    return update_resource(TRAININGS_PATH, training.training_id, training)

def update_training_entry(entry: TrainingEntry) -> JSONResponse:
    return update_resource(TRAINING_ENTRIES_PATH, entry.training_id, entry)

def invalidate_entries(racer_id: str) -> None:
    entry_list: list[dict] = get_all_resources(TRAINING_ENTRIES_PATH)
    for entry_dict in entry_list:
        entry: TrainingEntry = TrainingEntry(**entry_dict)
        if entry.status != "finished":
            training_dict: dict|None = get_resource(TRAININGS_PATH, entry.training_id, ["setup"])
            if training_dict is not None:
                setup: dict = training_dict["setup"]
                if setup["racer_id"] == racer_id:
                    if entry.status == "created":
                        entry.status = "deprecated"
                        update_training_entry(entry)
                    elif entry.status == "running":
                        entry.status = "interrupted"
                        entry.finished_at = now()
                        update_training_entry(entry)