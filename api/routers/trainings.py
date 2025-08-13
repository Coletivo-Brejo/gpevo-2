from datetime import datetime
from fastapi import APIRouter, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import os

from .runs import RUNS_PATH
from data_manager import (
    get_training_info_with_filters,
    invalidate_entries,
    update_brain,
    update_training,
    update_training_entry,
)
from models.training import IterationUpdate, Training, TrainingEntry, TrainingInfo, TrainingSetup
from routers.runs import save_runs
from utils import (
    delete_resource,
    get_next_id,
    get_resource,
    now,
    read_all_resources,
    read_resource,
)


TRAININGS_PATH = "{data_path}/trainings".format(
    data_path = os.environ.get("DATA_PATH")
)
TRAINING_ENTRIES_PATH = f"{TRAININGS_PATH}/entries"

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
    return JSONResponse(jsonable_encoder(get_training_info_with_filters(racer_ids, track_ids)))

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
