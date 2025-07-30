from datetime import datetime
from dotenv import load_dotenv
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import os

from models.training import Training, TrainingEntry
from utils import (
    get_all_resources,
    get_next_id,
    get_resource,
    now,
    read_all_resources,
    read_resource,
    update_resource,
)


load_dotenv()
TRAININGS_PATH = "{data_path}/trainings".format(
    data_path = os.environ.get("DATA_PATH")
)
TRAINING_ENTRIES_PATH = "{data_path}/training_entries".format(
    data_path = os.environ.get("DATA_PATH")
)

def update_training_entry(entry: TrainingEntry) -> None:
    update_resource(TRAINING_ENTRIES_PATH, entry.training_id, entry)

router = APIRouter()

@router.get("/trainings")
def read_trainings(
        fields: list[str] = Query(None),
    ) -> JSONResponse:
    return read_all_resources(TRAININGS_PATH, fields)

@router.get("/trainings/new")
def create_training_entry() -> JSONResponse:
    entry_list: list[dict] = get_all_resources(TRAINING_ENTRIES_PATH)
    for entry_dict in entry_list:
        entry: TrainingEntry = TrainingEntry(**entry_dict)
        if entry.status != "finished":
            training_dict: dict|None = get_resource(TRAININGS_PATH, entry.training_id, ["racer_id"])
            if training_dict is not None:
                training: Training = Training(**training_dict)
                
        if entry.status == "created":
            entry.status = "deprecated"
            update_training_entry(entry)
        elif entry.status == "running":
            entry.status = "interrupted"
            entry.finished_at = now()
            update_training_entry(entry)
    training_id: str = get_next_id("training_id", "training_{id}")
    creation_dt: datetime = now()
    new_entry: TrainingEntry = TrainingEntry(
        training_id = training_id,
        status = "created",
        created_at = creation_dt,
    )
    update_training_entry(new_entry)
    return read_resource(TRAINING_ENTRIES_PATH, training_id)

@router.get("/trainings/{training_id}")
def read_training(
        training_id: str,
        fields: list[str] = Query(None),
    ) -> JSONResponse:
    return read_resource(TRAININGS_PATH, training_id, fields)

@router.put("/trainings/{training_id}")
def update_training(training_id: str, training: Training):
    entry_dict: dict|None = get_resource(TRAINING_ENTRIES_PATH, training_id)
    if entry_dict is not None:
        entry: TrainingEntry = TrainingEntry(**entry_dict)
        if training.end_reason != "" and entry.finished_at is None:
            entry.status = "finished"
            entry.finished_at = now()
        elif training.end_reason == "":
            entry.status = "running"
        update_training_entry(entry)
    return update_resource(TRAININGS_PATH, training_id, training)

@router.get("/trainings/entries")
def read_training_entries(
        fields: list[str] = Query(None),
    ) -> JSONResponse:
    return read_all_resources(TRAINING_ENTRIES_PATH, fields)