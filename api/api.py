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

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World", "path": os.environ.get("DATA_PATH")}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

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
    