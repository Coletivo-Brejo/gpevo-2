from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os

from models.brain import Brain, MutationSetup
from models.models import (
    Racer,
    Run,
    Ship,
    Track,
)
from routers import trainings
from utils import (
    get_next_id,
    read_resource,
    read_all_resources,
    update_resource,
)


logging.basicConfig(level=logging.WARNING)

load_dotenv()
DATA_PATH = os.environ.get("DATA_PATH")
TRACKS_PATH = f"{DATA_PATH}/tracks"
SHIPS_PATH = f"{DATA_PATH}/ships"
RACERS_PATH = f"{DATA_PATH}/racers"
RUNS_PATH = f"{DATA_PATH}/runs"

app = FastAPI()
app.include_router(trainings.router)
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

@app.get("/ids/next")
def get_id(
        id_name: str,
        id_format: str = "{id}",
    ) -> JSONResponse:
    next_id: str = get_next_id(id_name, id_format)
    return JSONResponse({id_name: next_id})

@app.get("/tracks")
def read_tracks(
        fields: list[str] = Query(None),
    ) -> JSONResponse:
    return read_all_resources(TRACKS_PATH, fields)

@app.get("/tracks/{track_id}")
def read_track(
        track_id: str,
        fields: list[str] = Query(None),
    ) -> JSONResponse:
    return read_resource(TRACKS_PATH, track_id, fields)

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

@app.post("/mutate")
def mutate_brain(
        brain: Brain,
        mutation_setup: MutationSetup,
    ):
    return brain.mutate(mutation_setup)