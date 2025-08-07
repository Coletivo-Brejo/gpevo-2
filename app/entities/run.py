from __future__ import annotations
import numpy as np
import streamlit as st

from .point import PointList
from .track import Track
from utils.proxy import load_resource_dict


@st.cache_data
def load_run(
        run_id: str,
        fields: list[str]|None = None,
    ) -> Run|None:
    run_dict: dict|None = load_resource_dict("/runs", run_id, fields)
    if run_dict is not None:
        run: Run = Run.from_dict(run_dict)
        return run
    else:
        return None


class RunStats():
    
    racer_id: str
    track_id: str
    lap: int
    time: float
    max_progress: float
    finished: bool
    stuck: bool
    time_history: np.ndarray
    progress_history: np.ndarray
    position_history: PointList
    activation_history: dict[str, np.ndarray]

    def __init__(
            self,
            _racer_id: str,
            _track_id: str,
            _lap: int,
            _time: float,
            _max_progress: float,
            _finished: bool,
            _stuck: bool,
            _time_history: np.ndarray,
            _progress_history: np.ndarray,
            _position_history: PointList,
            _activation_history: dict[str, np.ndarray]
        ) -> None:
        self.racer_id = _racer_id
        self.track_id = _track_id
        self.lap = _lap
        self.time = _time
        self.max_progress = _max_progress
        self.finished = _finished
        self.stuck = _stuck
        self.time_history = _time_history
        self.progress_history = _progress_history
        self.position_history = _position_history
        self.activation_history = _activation_history
    
    @staticmethod
    def from_dict(
            _dict: dict,
        ) -> RunStats:
        return RunStats(
            _dict["racer_id"],
            _dict["track_id"],
            _dict["lap"],
            _dict["time"],
            _dict["max_progress"],
            _dict["finished"],
            _dict["stuck"],
            np.array(_dict["time_history"]),
            np.array(_dict["progress_history"]),
            PointList.from_list(_dict["position_history"]),
            {k:np.array(v) for k, v in _dict["activation_history"].items()},
        )

    def generate_history_traces(self) -> list[dict]:
        traces: list[dict] = [
            {
                "type": "scatter",
                "mode": "markers",
                "x": self.position_history.xs(),
                "y": self.position_history.ys(),
                "line": {
                    "color": "grey",
                },
            }
        ]
        return traces
    
    def generate_progress_traces(self) -> list[dict]:
        traces: list[dict] = [
            {
                "type": "scatter",
                "mode": "lines",
                "x": self.time_history,
                "y": self.progress_history,
            }
        ]
        return traces
    
    def generate_eeg_traces(self) -> list[dict]:
        traces: list[dict] = []
        for n, values in self.activation_history.items():
            traces.append(
                {
                    "type": "scatter",
                    "mode": "lines",
                    "name": n,
                    "x": self.time_history,
                    "y": values,
                    "legendgroup": "sensors" if n.startswith("s") or n.startswith("v") else "thrusters" if n.startswith("t") else "neurons",
                    "legendgrouptitle_text": "sensors" if n.startswith("s") or n.startswith("v") else "thrusters" if n.startswith("t") else "neurons",
                    # "showlegend": False,
                }
            )
        return traces


class RunSetup():

    begin_countdown: float
    end_countdown: float
    stuck_timeout: float
    run_timeout: float
    follow_first: bool
    end_on_first_finish: bool
    stat_collection_frequency: float
    mirrored: bool
    laps: int

    def __init__(
            self,
            _begin_countdown: float,
            _end_countdown: float,
            _stuck_timeout: float,
            _run_timeout: float,
            _follow_first: bool,
            _end_on_first_finish: bool,
            _stat_collection_frequency: float,
            _mirrored: bool,
            _laps: int,
        ) -> None:
        self.begin_countdown = _begin_countdown
        self.end_countdown = _end_countdown
        self.stuck_timeout = _stuck_timeout
        self.run_timeout = _run_timeout
        self.follow_first = _follow_first
        self.end_on_first_finish = _end_on_first_finish
        self.stat_collection_frequency = _stat_collection_frequency
        self.mirrored = _mirrored
        self.laps = _laps
    
    @staticmethod
    def from_dict(
            _dict: dict,
        ) -> RunSetup:
        return RunSetup(
            _dict["begin_countdown"],
            _dict["end_countdown"],
            _dict["stuck_timeout"],
            _dict["run_timeout"],
            _dict["follow_first"],
            _dict["end_on_first_finish"],
            _dict["stat_collection_frequency"],
            _dict["mirrored"],
            _dict["laps"],
        )
    
    def to_dict(self) -> dict:
        return {
            "begin_countdown": self.begin_countdown,
            "end_countdown": self.end_countdown,
            "stuck_timeout": self.stuck_timeout,
            "run_timeout": self.run_timeout,
            "follow_first": self.follow_first,
            "end_on_first_finish": self.end_on_first_finish,
            "stat_collection_frequency": self.stat_collection_frequency,
            "mirrored": self.mirrored,
            "laps": self.laps,
        }


class Run():

    run_id: str
    track_id: str
    racer_ids: list[str]
    setup: RunSetup
    elapsed_time: float
    end_reason: str
    stats: list[RunStats]

    track: Track|None

    def __init__(
            self,
            _run_id: str,
            _track_id: str,
            _racer_ids: list[str],
            _setup: RunSetup,
            _elapsed_time: float,
            _end_reason: str,
            _stats: list[RunStats],
            _track: Track|None = None,
        ) -> None:
        self.run_id = _run_id
        self.track_id = _track_id
        self.racer_ids = _racer_ids
        self.setup = _setup
        self.elapsed_time = _elapsed_time
        self.end_reason = _end_reason
        self.stats = _stats

        if _track is not None:
            self.track = _track
        else:
            self.track = Track.load(self.track_id)
    
    @staticmethod
    def from_dict(
            _dict: dict,
            _track: Track|None = None,
        ) -> Run:
        return Run(
            _dict["run_id"],
            _dict["track_id"],
            _dict["racer_ids"],
            RunSetup.from_dict(_dict["setup"]),
            _dict["elapsed_time"],
            _dict["end_reason"],
            [RunStats.from_dict(s) for s in _dict["stats"]],
            _track,
        )
    
    @staticmethod
    def load(
            run_id: str,
            fields: list[str]|None = None,
        ) -> Run|None:
        return load_run(run_id, fields)
    
    def get_stats_from_racer(
            self,
            racer_id: str,
        ) -> RunStats|None:
        for s in self.stats:
            if s.racer_id == racer_id:
                return s
        return None

    def generate_racer_history_traces(
            self,
            racer_id: str
        ) -> list[dict]:
        traces: list[dict] = []
        if self.track is not None:
            traces.extend(self.track.generate_traces(self.setup.mirrored))
        stat: RunStats|None = self.get_stats_from_racer(racer_id)
        if stat is not None:
            traces.extend(stat.generate_history_traces())
        return traces
    
    def generate_racer_progress_traces(
            self,
            racer_id: str,
        ) -> list[dict]:
        stat: RunStats|None = self.get_stats_from_racer(racer_id)
        if stat is not None:
            return stat.generate_progress_traces()
        return []
    
    def generate_racer_eeg_traces(
            self,
            racer_id: str,
        ) -> list[dict]:
        stat: RunStats|None = self.get_stats_from_racer(racer_id)
        if stat is not None:
            return stat.generate_eeg_traces()
        return []