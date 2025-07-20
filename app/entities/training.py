from __future__ import annotations
from dotenv import load_dotenv
import numpy as np
import os
import requests

from .run import Run, RunStats
from .track import Track


load_dotenv()
API_URL = os.environ.get("API_URL")

class Training():

    training_id: str
    track_id: str
    racer_id: str
    save_results: bool
    run_data: Run
    n_neighbors: int
    initial_temperature: float
    cooling_rate: float
    convergence_threshold: float
    convergence_iterations: int
    n_iterations: int
    progress_objective: float
    time_objective: float
    max_training_time: float
    run_history: list[Run]
    racer_history: list[RunStats]
    elapsed_time: float
    end_reason: str

    track: Track

    def __init__(
            self,
            _training_id: str,
            _track_id: str,
            _racer_id: str,
            _save_results: bool,
            _run_data: Run,
            _n_neighbors: int,
            _initial_temperature: float,
            _cooling_rate: float,
            _convergence_threshold: float,
            _convergence_iterations: int,
            _n_iterations: int,
            _progress_objective: float,
            _time_objective: float,
            _max_training_time: float,
            _run_history: list[Run],
            _racer_history: list[RunStats],
            _elapsed_time: float,
            _end_reason: str,
        ) -> None:
        self.training_id = _training_id
        self.track_id = _track_id
        self.racer_id = _racer_id
        self.save_results = _save_results
        self.run_data = _run_data
        self.n_neighbors = _n_neighbors
        self.initial_temperature = _initial_temperature
        self.cooling_rate = _cooling_rate
        self.convergence_threshold = _convergence_threshold
        self.convergence_iterations = _convergence_iterations
        self.n_iterations = _n_iterations
        self.progress_objective = _progress_objective
        self.time_objective = _time_objective
        self.max_training_time = _max_training_time
        self.run_history = _run_history
        self.racer_history = _racer_history
        self.elapsed_time = _elapsed_time
        self.end_reason = _end_reason

        self.request_track()
    
    @staticmethod
    def from_dict(_dict: dict) -> Training:
        return Training(
            _dict["training_id"],
            _dict["track_id"],
            _dict["racer_id"],
            _dict["save_results"],
            Run.from_dict(_dict["run_data"]),
            _dict["n_neighbors"],
            _dict["initial_temperature"],
            _dict["cooling_rate"],
            _dict["convergence_threshold"],
            _dict["convergence_iterations"],
            _dict["n_iterations"],
            _dict["progress_objective"],
            _dict["time_objective"],
            _dict["max_training_time"],
            [Run.from_dict(r) for r in _dict["run_history"]],
            [RunStats.from_dict(r) for r in _dict["racer_history"]],
            _dict["elapsed_time"],
            _dict["end_reason"],
        )
    
    def request_track(self) -> None:
        response = requests.get(f"{API_URL}/tracks/{self.track_id}")
        if response.ok:
            track_dict: dict = response.json()
            self.track = Track.from_dict(track_dict)

    def generate_progress_evolution_traces(self) -> list[dict]:
        progress: np.ndarray = np.array([r.max_progress for r in self.racer_history])
        traces: list[dict] = [
            {
                "type": "scatter",
                "mode": "markers+lines",
                "x": [i for i in range(len(progress))],
                "y": progress,
            }
        ]
        return traces

    def generate_progress_traces(
            self,
            iteration: int = 0,
        ) -> list[dict]:
        return self.racer_history[iteration].generate_progress_traces()

    def generate_history_traces(
            self,
            iteration: int = 0,
        ) -> list[dict]:
        traces: list[dict] = []
        traces.extend(
            self.track.generate_traces(self.run_data.mirrored))
        traces.extend(
            self.racer_history[iteration].generate_history_traces(
                self.run_data.mirrored,
            )
        )
        return traces