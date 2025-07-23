from __future__ import annotations
import numpy as np

from .run import Run, RunStats
from .track import Track


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
    greedy: bool
    prob_create_neuron: float
    prob_delete_neuron: float
    prob_create_connection: float
    prob_delete_connection: float
    run_history: list[Run]
    racer_history: list[RunStats]
    elapsed_time: float
    end_reason: str

    track: Track|None

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
            _greedy: bool,
            _prob_create_neuron: float,
            _prob_delete_neuron: float,
            _prob_create_connection: float,
            _prob_delete_connection: float,
            _run_history: list[Run],
            _racer_history: list[RunStats],
            _elapsed_time: float,
            _end_reason: str,
            _track: Track|None = None,
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
        self.greedy = _greedy
        self.prob_create_neuron = _prob_create_neuron
        self.prob_delete_neuron = _prob_delete_neuron
        self.prob_create_connection = _prob_create_connection
        self.prob_delete_connection = _prob_delete_connection
        self.run_history = _run_history
        self.racer_history = _racer_history
        self.elapsed_time = _elapsed_time
        self.end_reason = _end_reason

        if _track is not None:
            self.track = _track
        else:
            self.track = Track.load(self.track_id)
    
    @staticmethod
    def from_dict(
            _dict: dict,
            _track: Track|None = None,
        ) -> Training:
        if _track is None:
            _track = Track.load(_dict["track_id"])
        return Training(
            _dict["training_id"],
            _dict["track_id"],
            _dict["racer_id"],
            _dict["save_results"],
            Run.from_dict(_dict["run_data"], _track),
            _dict["n_neighbors"],
            _dict["initial_temperature"],
            _dict["cooling_rate"],
            _dict["convergence_threshold"],
            _dict["convergence_iterations"],
            _dict["n_iterations"],
            _dict["progress_objective"],
            _dict["time_objective"],
            _dict["max_training_time"],
            _dict["greedy"],
            _dict["prob_create_neuron"],
            _dict["prob_delete_neuron"],
            _dict["prob_create_connection"],
            _dict["prob_delete_connection"],
            [Run.from_dict(r, _track) for r in _dict["run_history"]],
            [RunStats.from_dict(r, _track) for r in _dict["racer_history"]],
            _dict["elapsed_time"],
            _dict["end_reason"],
            _track,
        )

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

    def generate_time_evolution_traces(self) -> list[dict]:
        time: np.ndarray = np.array([r.time if r.finished else None for r in self.racer_history ])
        traces: list[dict] = [
            {
                "type": "scatter",
                "mode": "markers+lines",
                "x": [i for i in range(len(time))],
                "y": time,
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
        if self.track is not None:
            traces.extend(
                self.track.generate_traces(self.run_data.mirrored))
        traces.extend(
            self.racer_history[iteration].generate_history_traces()
        )
        return traces