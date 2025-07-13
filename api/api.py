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
    core: list[Point]
    l_wall: list[Point]
    r_wall: list[Point]

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
    thrusters: list[Thruster]
    sensors: list[SensorSet]

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/tracks")
def read_tracks():
    tracks: list[dict] = []
    for file in os.listdir(TRACKS_PATH):
        track_file: str = f"{TRACKS_PATH}/{file}"
        with open(track_file) as f:
            track_dict: dict = json.load(f)
            tracks.append(track_dict)
    return JSONResponse(tracks)

@app.get("/tracks/{track_id}")
def read_track(track_id: str):
    track_file = f"{TRACKS_PATH}/{track_id}.json"
    try:
        with open(track_file) as f:
            track_dict: dict = json.load(f)
            return JSONResponse(track_dict)
    except:
        return JSONResponse("Pista não encontrada", status_code=404)

@app.put("/tracks/{track_id}")
def update_track(track_id: str, track: Track):
    if not os.path.exists(TRACKS_PATH):
        os.makedirs(TRACKS_PATH)
    track_file: str = f"{TRACKS_PATH}/{track_id}.json"
    with open(track_file, "w", encoding="utf-8") as f:
        track_json = jsonable_encoder(track)
        json.dump(track_json, f, ensure_ascii=False)
    return JSONResponse("Pista salva")

@app.get("/ships")
def read_ships():
    ships: list[dict] = []
    for file in os.listdir(SHIPS_PATH):
        ship_file: str = f"{SHIPS_PATH}/{file}"
        with open(ship_file) as f:
            ship_dict: dict = json.load(f)
            ships.append(ship_dict)
    return JSONResponse(ships)

@app.get("/ships/{ship_id}")
def read_ship(ship_id: str):
    ship_file = f"{SHIPS_PATH}/{ship_id}.json"
    try:
        with open(ship_file) as f:
            ship_dict: dict = json.load(f)
            return JSONResponse(ship_dict)
    except:
        return JSONResponse("Nave não encontrada", status_code=404)

@app.put("/ships/{ship_id}")
def update_ship(ship_id: str, ship: Ship):
    if not os.path.exists(SHIPS_PATH):
        os.makedirs(SHIPS_PATH)
    ship_file: str = f"{SHIPS_PATH}/{ship_id}.json"
    with open(ship_file, "w", encoding="utf-8") as f:
        ship_json = jsonable_encoder(ship)
        json.dump(ship_json, f, ensure_ascii=False)
    return JSONResponse("Nave salva")