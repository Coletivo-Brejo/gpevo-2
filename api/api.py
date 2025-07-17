from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import json
import os
from pydantic import BaseModel
from typing import Union


load_dotenv()
DATA_PATH = os.environ.get("DATA_PATH")
TRACKS_PATH = f"{DATA_PATH}/tracks"
SHIPS_PATH = f"{DATA_PATH}/ships"
RACERS_PATH = f"{DATA_PATH}/racers"
RUNS_PATH = f"{DATA_PATH}/runs"

class Point(BaseModel):
    x: float
    y: float

class TrackSegment(BaseModel):
    length: float
    curvature: float
    l_wall_dist: float
    l_wall_curv: float
    r_wall_dist: float
    r_wall_curv: float

class Track(BaseModel):
    track_id: str
    name: str
    segments: list[TrackSegment]
    loops: bool
    core: list[Point]
    l_wall: list[Point]
    r_wall: list[Point]
    length: float

class Thruster(BaseModel):
    power: float
    texture: str
    position: Point
    rotation: float

class SensorSet(BaseModel):
    amount: int
    aperture: float
    reach: float
    texture: str
    position: Point
    rotation: float

class Ship(BaseModel):
    ship_id: str
    name: str
    mass: float
    chassis_texture: str
    chassis_collision: list[Point]
    thrusters: list[Thruster]
    sensors: list[SensorSet]

class Operation(BaseModel):
    type: str
    params: list[float]

class Neuron(BaseModel):
    neuron_id: str
    max_inputs: int
    input_ids: list[str]
    operations: list[Operation]

class Brain(BaseModel):
    neurons: list[Neuron]
    current_id: int

class Racer(BaseModel):
    racer_id: str
    name: str
    brain: Brain
    ship: Ship

class RunStats(BaseModel):
    racer_id: str
    track_id: str
    lap: int
    max_progress: float
    finished: bool
    stuck: bool
    time_history: list[float]
    progress_history: list[float]
    position_history: list[Point]

class Run(BaseModel):
    run_id: str
    track_id: str
    racer_ids: list[str]
    begin_countdown: float
    end_countdown: float
    stuck_timeout: float
    run_timeout: float
    end_on_first_finish: bool
    stat_collection_frequency: float
    mirrored: bool
    laps: int
    elapsed_time: float
    stats: list[RunStats]

def read_resource(
        dir: str,
        resource_id: str
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
    ) -> JSONResponse:
    resources: list[dict] = []
    for file in os.listdir(dir):
        resource_file: str = f"{dir}/{file}"
        with open(resource_file) as f:
            resource_dict: dict = json.load(f)
            resources.append(resource_dict)
    return JSONResponse(resources)

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

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/tracks")
def read_tracks():
    return read_all_resources(TRACKS_PATH)

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
def read_racers():
    return read_all_resources(RACERS_PATH)

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