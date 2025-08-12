from datetime import datetime
from fastapi import APIRouter, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import os

from .runs import RUNS_PATH
from data_manager import update_brain
from models.training import IterationUpdate, Training, TrainingEntry, TrainingInfo, TrainingSetup
from routers.runs import save_runs
from utils import (
    delete_resource,
    get_all_resources,
    get_next_id,
    get_resource,
    now,
    read_all_resources,
    read_resource,
    update_resource,
)


TRAININGS_PATH = "{data_path}/trainings".format(
    data_path = os.environ.get("DATA_PATH")
)
TRAINING_ENTRIES_PATH = f"{TRAININGS_PATH}/entries"
TRACKS_PATH = f"{os.environ.get('DATA_PATH')}/tracks"
RACERS_PATH = f"{os.environ.get('DATA_PATH')}/racers"

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

def get_info_with_filters(
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

router = APIRouter()

@router.get("/trainings")
def read_trainings(
        fields: list[str] = Query(None),
    ) -> JSONResponse:
    return read_all_resources(TRAININGS_PATH, fields)

@router.get("/trainings/entries")
def read_training_entries(
        fields: list[str] = Query(None),
    ) -> JSONResponse:
    return read_all_resources(TRAINING_ENTRIES_PATH, fields)

@router.get("/trainings/info")
def read_training_info(
        racer_ids: list[str] = Query(None),
        track_ids: list[str] = Query(None),
    ) -> JSONResponse:
    return JSONResponse(jsonable_encoder(get_info_with_filters(racer_ids, track_ids)))

@router.post("/trainings/new")
def create_training(setup: TrainingSetup) -> JSONResponse:
    invalidate_entries(setup.racer_id)
    training_id: str = get_next_id("training_id", "training_{id}")
    creation_dt: datetime = now()
    new_entry: TrainingEntry = TrainingEntry(
        training_id = training_id,
        status = "created",
        created_at = creation_dt,
    )
    update_training_entry(new_entry)
    new_training: Training = Training(
        training_id = training_id,
        setup = setup,
        iteration = 0,
        convergence_iteration = 0,
        temperature = setup.initial_temperature,
        run_id_history = [],
        clone_history = [],
        brain_history = [],
        elapsed_time = 0.,
        end_reason = "",
    )
    update_training(new_training)
    return read_resource(TRAINING_ENTRIES_PATH, training_id)

@router.put("/trainings")
def save_training(training: Training) -> JSONResponse:
    training_id: str = training.training_id
    entry_dict: dict|None = get_resource(TRAINING_ENTRIES_PATH, training_id)
    if entry_dict is not None:
        entry: TrainingEntry = TrainingEntry(**entry_dict)
        if entry.status not in {"finished", "deprecated", "interrupted"}:
            if training.end_reason != "":
                entry.status = "finished"
                entry.finished_at = now()
            elif training.end_reason == "":
                entry.status = "running"
            update_training_entry(entry)
            return update_training(training)
        else:
            return JSONResponse({"Erro": "Treinamento já concluído ou interrompido"}, status_code = 400)
    else:
        return JSONResponse({"Erro": "Treinamento não encontrado"}, status_code = 404)

@router.get("/trainings/{training_id}")
def read_training(
        training_id: str,
        fields: list[str] = Query(None),
    ) -> JSONResponse:
    return read_resource(TRAININGS_PATH, training_id, fields)

@router.delete("/trainings/{training_id}")
def delete_training(
        training_id: str,
    ) -> JSONResponse:
    run_ids: list[str] = []
    training_dict: dict|None = get_resource(TRAININGS_PATH, training_id, ["run_id_history"])
    if training_dict is not None:
        for it in training_dict["run_id_history"]:
            for run_id in it:
                run_ids.append(run_id)
    runs_deleted: int = 0
    runs_not_deleted: int = 0
    for run_id in run_ids:
        run_deleted: bool = delete_resource(RUNS_PATH, run_id)
        if run_deleted:
            runs_deleted += 1
        else:
            runs_not_deleted += 1
    entry_deleted: bool = delete_resource(TRAINING_ENTRIES_PATH, training_id)
    training_deleted: bool = delete_resource(TRAININGS_PATH, training_id)
    return JSONResponse(
        {
            "Training deleted": training_deleted,
            "Entry deleted": entry_deleted,
            "Runs deleted": runs_deleted,
            "Runs not deleted": runs_not_deleted,
        }
    )

@router.post("/trainings/{training_id}/save_iteration")
def save_training_iteration(
        training_id: str,
        iteration_data: IterationUpdate,
    ) -> JSONResponse:
    response: JSONResponse = save_training(iteration_data.training)
    if response.status_code == 200:
        save_runs(iteration_data.runs)
        racer_id: str = iteration_data.training.setup.racer_id
        racer_response:JSONResponse = update_brain(racer_id, iteration_data.brain)
        if racer_response.status_code == 200:
            return JSONResponse({"Sucesso": "Treinamento atualizado"})
        else:
            return racer_response
    else:
        return response
