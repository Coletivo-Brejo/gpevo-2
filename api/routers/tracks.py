from fastapi import APIRouter, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import os

from models.track import LeaderboardEntry, Track, TrackLeaderboard
from data_manager import get_leaderboard
from utils import (
    read_all_resources,
    read_resource,
    update_resource,
)


TRACKS_PATH = "{data_path}/tracks".format(
    data_path = os.environ.get("DATA_PATH")
)
LEADERBOARDS_PATH = f"{TRACKS_PATH}/leaderboards"

router = APIRouter()

@router.get("/tracks")
def read_tracks(
        fields: list[str] = Query(None),
    ) -> JSONResponse:
    return read_all_resources(TRACKS_PATH, fields)

@router.get("/tracks/{track_id}")
def read_track(
        track_id: str,
        fields: list[str] = Query(None),
    ) -> JSONResponse:
    return read_resource(TRACKS_PATH, track_id, fields)

@router.put("/tracks/{track_id}")
def update_track(track_id: str, track: Track):
    return update_resource(TRACKS_PATH, track_id, track)

@router.get("/tracks/{track_id}/leaderboard")
def retrieve_leaderboard(
        track_id: str,
    ) -> JSONResponse:
    return JSONResponse(jsonable_encoder(get_leaderboard(track_id)))

@router.get("/tracks/{track_id}/leaderboard/entries/{mode}")
def query_leaderboard(
        track_id: str,
        mode: str,
        racer_id: str = Query(None),
        mirrored: bool = Query(None),
        laps: int = Query(None),
    ) -> JSONResponse:
    leaderboard: TrackLeaderboard = get_leaderboard(track_id)
    entries: list[LeaderboardEntry] = []
    if mode == "best":
        entries = leaderboard.best_entries
    elif mode == "latest":
        entries = leaderboard.latest_entries
    if racer_id is not None:
        entries = [e for e in entries if e.racer_id == racer_id]
    if mirrored is not None:
        entries = [e for e in entries if e.mirrored == mirrored]
    if laps is not None:
        entries = [e for e in entries if e.laps == laps]
    finished_entries: list[LeaderboardEntry] = [e for e in entries if e.finished]
    finished_entries.sort(key = lambda entry: entry.time)
    unfinished_entries: list[LeaderboardEntry] = [e for e in entries if not e.finished]
    unfinished_entries.sort(key = lambda entry: entry.progress, reverse = True)
    entries = finished_entries + unfinished_entries
    return JSONResponse(jsonable_encoder(entries))