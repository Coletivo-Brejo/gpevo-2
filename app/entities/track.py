from __future__ import annotations
from datetime import datetime
import numpy as np
import streamlit as st

from .point import PointList
from utils.proxy import load_resource_dict


@st.cache_data
def load_track(
        track_id: str,
        fields: list[str]|None = None,
    ) -> Track|None:
    track_dict: dict|None = load_resource_dict("/tracks", track_id, fields)
    if track_dict is not None:
        track: Track = Track.from_dict(track_dict)
        return track
    else:
        return None


class Track():

    track_id: str
    name: str
    loops: bool
    core: PointList
    l_wall: PointList
    r_wall: PointList
    length: float

    def __init__(
            self,
            _track_id: str,
            _name: str,
            _loops: bool,
            _core: PointList,
            _l_wall: PointList,
            _r_wall: PointList,
            _length: float,
        ) -> None:
        self.track_id = _track_id
        self.name = _name
        self.loops = _loops
        self.core = _core
        self.l_wall = _l_wall
        self.r_wall = _r_wall
        self.length = _length
    
    @staticmethod
    def from_dict(_dict: dict) -> Track:
        return Track(
            _dict["track_id"],
            _dict["name"],
            _dict["loops"],
            PointList.from_list(_dict["core"]),
            PointList.from_list(_dict["l_wall"]),
            PointList.from_list(_dict["r_wall"]),
            _dict["length"],
        )
    
    @staticmethod
    def load(
            track_id: str,
            fields: list[str]|None = None,
        ) -> Track|None:
        return load_track(track_id, fields)
    
    def generate_traces(
            self,
            mirrored: bool = False,
        ) -> list[dict]:

        x_scale: float = -1. if mirrored else 1.
        l_xs: np.ndarray = self.l_wall.xs() * x_scale
        l_ys: np.ndarray = self.l_wall.ys()
        r_xs: np.ndarray = self.r_wall.xs() * x_scale
        r_ys: np.ndarray = self.r_wall.ys()

        traces: list[dict] = [
            {
                "type": "scatter",
                "mode": "lines",
                "x": l_xs,
                "y": l_ys,
                "line": {
                    "color": "grey",
                },
            },
            {
                "type": "scatter",
                "mode": "lines",
                "x": r_xs,
                "y": r_ys,
                "line": {
                    "color": "grey",
                },
            },
            {
                "type": "scatter",
                "mode": "lines",
                "x": [l_xs[0], r_xs[0]],
                "y": [l_ys[0], r_ys[0]],
                "line": {
                    "color": "grey",
                },
            },
        ]
        if not self.loops:
            traces.append(
                {
                    "type": "scatter",
                    "mode": "lines",
                    "x": [l_xs[-1], r_xs[-1]],
                    "y": [l_ys[-1], r_ys[-1]],
                    "line": {
                        "color": "grey",
                    },
                },
            )
        return traces


class LeaderboardEntry():
    track_id: str
    racer_id: str
    brain_version: int
    run_id: str
    ran_at: datetime
    mirrored: bool
    laps: int
    progress: float
    time: float
    finished: bool

    def __init__(
            self,
            _track_id: str,
            _racer_id: str,
            _brain_version: int,
            _run_id: str,
            _ran_at: datetime,
            _mirrored: bool,
            _laps: int,
            _progress: float,
            _time: float,
            _finished: bool,
        ) -> None:
        self.track_id = _track_id
        self.racer_id = _racer_id
        self.brain_version = _brain_version
        self.run_id = _run_id
        self.ran_at = _ran_at
        self.mirrored = _mirrored
        self.laps = _laps
        self.progress = _progress
        self.time = _time
        self.finished = _finished
    
    @staticmethod
    def from_dict(_dict: dict) -> LeaderboardEntry:
        return LeaderboardEntry(
            _dict["track_id"],
            _dict["racer_id"],
            _dict["brain_version"],
            _dict["run_id"],
            datetime.strptime(_dict["ran_at"], "%Y-%m-%dT%H:%M:%S.%f%z"),
            _dict["mirrored"],
            _dict["laps"],
            _dict["progress"],
            _dict["time"],
            _dict["finished"],
        )


class TrackLeaderboard():
    track_id: str
    latest_entries: list[LeaderboardEntry]
    best_entries: list[LeaderboardEntry]

    def __init__(
            self,
            _track_id: str,
            _latest_entries: list[LeaderboardEntry],
            _best_entries: list[LeaderboardEntry],
        ) -> None:
        self.track_id = _track_id
        self.latest_entries = _latest_entries
        self.best_entries = _best_entries
    
    @staticmethod
    def from_dict(_dict: dict) -> TrackLeaderboard:
        return TrackLeaderboard(
            _dict["track_id"],
            [LeaderboardEntry.from_dict(e) for e in _dict["latest_entries"]],
            [LeaderboardEntry.from_dict(e) for e in _dict["best_entries"]],
        )