from __future__ import annotations
import numpy as np
import streamlit as st

from .point import PointList
from utils.proxy import load_resource_dict


@st.cache_data
def load_track(track_id: str) -> Track|None:
    track_dict: dict|None = load_resource_dict("/tracks", track_id)
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
    def load(track_id: str) -> Track|None:
        return load_track(track_id)
    
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