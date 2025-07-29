from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import logging
import os
from pydantic import BaseModel

from models.brain import Brain, MutationSetup
from models.models import (
    Racer,
    Run,
    Ship,
    Track,
)
from models.training import Training


logging.basicConfig(level=logging.WARNING)

load_dotenv()
DATA_PATH = os.environ.get("DATA_PATH")
TRACKS_PATH = f"{DATA_PATH}/tracks"
SHIPS_PATH = f"{DATA_PATH}/ships"
RACERS_PATH = f"{DATA_PATH}/racers"
RUNS_PATH = f"{DATA_PATH}/runs"
TRAININGS_PATH = f"{DATA_PATH}/trainings"

def read_resource(
        dir: str,
        resource_id: str,
    ) -> JSONResponse:
    resource_file = f"{dir}/{resource_id}.json"
    try:
        with open(resource_file, encoding="utf-8") as f:
            resource_dict: dict = json.load(f)
            return JSONResponse(resource_dict)
    except:
        return JSONResponse("Recurso não encontrado", status_code=404)

def read_all_resources(
        dir: str,
        fields: list[str]|None = None,
    ) -> JSONResponse:
    resources: list[dict] = []
    for file in os.listdir(dir):
        resource_file: str = f"{dir}/{file}"
        with open(resource_file, encoding="utf-8") as f:
            resource_dict: dict = json.load(f)
            if fields is not None:
                resource_dict = {k:v for k, v in resource_dict.items() if k in fields}
            resources.append(resource_dict)
    return JSONResponse(resources)

def read_all_resource_ids(
        dir: str,
    ) -> JSONResponse:
    resource_ids: list[str] = []
    for file in os.listdir(dir):
        if file.endswith(".json"):
            resource_ids.append(file[:-5])
    return JSONResponse(resource_ids)

def update_resource(
        dir: str,
        resource_id: str,
        resource: BaseModel
    ) -> JSONResponse:
    if not os.path.exists(dir):
        os.makedirs(dir)
    resource_file: str = f"{dir}/{resource_id}.json"
    with open(resource_file, "w", encoding="utf-8") as f:
        resource_json = jsonable_encoder(resource)
        json.dump(resource_json, f, ensure_ascii=False)
    return JSONResponse("Recurso atualizado")

app = FastAPI()
origins = [
    "http://localhost:8501",
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/tracks")
def read_tracks(
        fields: list[str] = Query(None),
    ) -> JSONResponse:
    return read_all_resources(TRACKS_PATH, fields)

@app.get("/tracks/ids")
def read_track_ids():
    return read_all_resource_ids(TRACKS_PATH)

@app.get("/tracks/{track_id}")
def read_track(track_id: str):
    return read_resource(TRACKS_PATH, track_id)

@app.put("/tracks/{track_id}")
def update_track(track_id: str, track: Track):
    return update_resource(TRACKS_PATH, track_id, track)

@app.get("/ships")
def read_ships():
    return read_all_resources(SHIPS_PATH)

@app.get("/ships/{ship_id}")
def read_ship(ship_id: str):
    return read_resource(SHIPS_PATH, ship_id)

@app.put("/ships/{ship_id}")
def update_ship(ship_id: str, ship: Ship):
    return update_resource(SHIPS_PATH, ship_id, ship)

@app.get("/racers")
def read_racers(
        fields: list[str] = Query(None),
    ) -> JSONResponse:
    return read_all_resources(RACERS_PATH, fields)

@app.get("/racers/ids")
def read_racer_ids():
    return read_all_resource_ids(RACERS_PATH)

@app.get("/racers/{racer_id}")
def read_racer(racer_id: str):
    return read_resource(RACERS_PATH, racer_id)

@app.put("/racers/{racer_id}")
def update_racer(racer_id: str, racer: Racer):
    return update_resource(RACERS_PATH, racer_id, racer)

@app.get("/runs")
def read_runs():
    return read_all_resources(RUNS_PATH)

@app.get("/runs/{run_id}")
def read_run(run_id: str):
    return read_resource(RUNS_PATH, run_id)

@app.put("/runs/{run_id}")
def update_run(run_id: str, run: Run):
    return update_resource(RUNS_PATH, run_id, run)

@app.get("/trainings")
def read_trainings():
    return read_all_resources(TRAININGS_PATH)

@app.get("/trainings/{training_id}")
def read_training(training_id: str):
    return read_resource(TRAININGS_PATH, training_id)

@app.put("/trainings/{training_id}")
def update_training(training_id: str, training: Training):
    return update_resource(TRAININGS_PATH, training_id, training)

@app.post("/mutate")
def mutate_brain(
        brain: Brain,
        mutation_setup: MutationSetup,
    ):
    return brain.mutate(mutation_setup)