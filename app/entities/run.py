from __future__ import annotations
import numpy as np

from .point import PointList


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
    
    @staticmethod
    def from_dict(_dict: dict) -> RunStats:
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
        )

    def generate_history_traces(
            self,
        ) -> list[dict]:

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
    
    def generate_progress_traces(
            self,
        ) -> list[dict]:
        
        traces: list[dict] = [
            {
                "type": "scatter",
                "mode": "lines",
                "x": self.time_history,
                "y": self.progress_history,
            }
        ]
        return traces


class Run():

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
    end_reason: str
    stats: list[RunStats]

    def __init__(
            self,
            _run_id: str,
            _track_id: str,
            _racer_ids: list[str],
            _begin_countdown: float,
            _end_countdown: float,
            _stuck_timeout: float,
            _run_timeout: float,
            _end_on_first_finish: bool,
            _stat_collection_frequency: float,
            _mirrored: bool,
            _laps: int,
            _elapsed_time: float,
            _end_reason: str,
            _stats: list[RunStats],
        ) -> None:
        self.run_id = _run_id
        self.track_id = _track_id
        self.racer_ids = _racer_ids
        self.begin_countdown = _begin_countdown
        self.end_countdown = _end_countdown
        self.stuck_timeout = _stuck_timeout
        self.run_timeout = _run_timeout
        self.end_on_first_finish = _end_on_first_finish
        self.stat_collection_frequency = _stat_collection_frequency
        self.mirrored = _mirrored
        self.laps = _laps
        self.elapsed_time = _elapsed_time
        self.end_reason = _end_reason
        self.stats = _stats
    
    @staticmethod
    def from_dict(_dict: dict) -> Run:
        return Run(
            _dict["run_id"],
            _dict["track_id"],
            _dict["racer_ids"],
            _dict["begin_countdown"],
            _dict["end_countdown"],
            _dict["stuck_timeout"],
            _dict["run_timeout"],
            _dict["end_on_first_finish"],
            _dict["stat_collection_frequency"],
            _dict["mirrored"],
            _dict["laps"],
            _dict["elapsed_time"],
            _dict["end_reason"],
            [RunStats.from_dict(s) for s in _dict["stats"]],
        )