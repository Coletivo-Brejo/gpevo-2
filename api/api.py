from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os

from models.brain import Brain, MutationSetup
from models.models import Racer, Ship, Track
from routers import runs, trainings
from routers.trainings import invalidate_entries
from utils import (
    get_next_id,
    get_resource,
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

app = FastAPI()
app.include_router(trainings.router)
app.include_router(runs.router)
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

@app.get("/racers/{racer_id}/lobotomize")
def lobotomize(
        racer_id: str,
        neurons: list[str] = Query(None),
    ) -> JSONResponse:
    racer_dict: dict|None = get_resource(RACERS_PATH, racer_id)
    deleted_neurons: list[str] = []
    removed_connections: list[str] = []
    reset_weights: list[str] = []
    if racer_dict is not None:
        racer: Racer = Racer(**racer_dict)
        for neuron in racer.brain.get_hidden_neurons():
            if neurons is None or neuron.neuron_id in neurons:
                deleted_neurons.append(neuron.neuron_id)
                racer.brain.delete_neuron(neuron)
        for neuron in racer.brain.get_thruster_neurons():
            if neurons is None or neuron.neuron_id in neurons:
                if len(neuron.input_ids) > 0:
                    removed_connections.append(neuron.neuron_id)
                    racer.brain.remove_all_inputs_from_neuron(neuron, True)
                reset_weights.append(neuron.neuron_id)
                racer.brain.reset_weights_from_neuron(neuron)
        update_resource(RACERS_PATH, racer_id, racer)
        invalidate_entries(racer_id)
        return JSONResponse({
            "Neurônios excluídos": deleted_neurons,
            "Conexões removidas": removed_connections,
            "Parâmetros zerados": reset_weights,
        })
    return JSONResponse({"Status": "Erro"})

@app.post("/mutate")
def mutate_brain(
        brain: Brain,
        mutation_setup: MutationSetup,
    ):
    return brain.mutate(mutation_setup)