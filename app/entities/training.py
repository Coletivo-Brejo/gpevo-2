from __future__ import annotations
from datetime import datetime
import numpy as np

from .brain import Brain, MutationSetup
from .run import Run, RunSetup, RunStats
from .track import Track


class TrainingRunSetup():

    track_id: str
    run_setup: RunSetup

    def __init__(
            self,
            _track_id: str,
            _run_setup: RunSetup,
        ) -> None:
        self.track_id = _track_id
        self.run_setup = _run_setup
    
    @staticmethod
    def from_dict(_dict: dict) -> TrainingRunSetup:
        return TrainingRunSetup(
            _dict["track_id"],
            RunSetup.from_dict(_dict["run_setup"]),
        )
    
    def to_dict(self) -> dict:
        return {
            "track_id": self.track_id,
            "run_setup": self.run_setup.to_dict(),
        }
    
class TrainingSetup():

    racer_id: str
    setups: list[TrainingRunSetup]
    save_results: bool
    initial_temperature: float
    cooling_rate: float
    convergence_threshold: float
    convergence_iterations: int
    n_iterations: int
    progress_objective: float
    time_objective: float
    max_training_time: float
    greedy: bool
    mutation_setup: MutationSetup

    def __init__(
            self,
            _racer_id: str,
            _setups: list[TrainingRunSetup],
            _save_results: bool,
            _initial_temperature: float,
            _cooling_rate: float,
            _convergence_threshold: float,
            _convergence_iterations: int,
            _n_iterations: int,
            _progress_objective: float,
            _time_objective: float,
            _max_training_time: float,
            _greedy: bool,
            _mutation_setup: MutationSetup,
        ) -> None:
        self.racer_id = _racer_id
        self.setups = _setups
        self.save_results = _save_results
        self.initial_temperature = _initial_temperature
        self.cooling_rate = _cooling_rate
        self.convergence_threshold = _convergence_threshold
        self.convergence_iterations = _convergence_iterations
        self.n_iterations = _n_iterations
        self.progress_objective = _progress_objective
        self.time_objective = _time_objective
        self.max_training_time = _max_training_time
        self.greedy = _greedy
        self.mutation_setup = _mutation_setup

    @staticmethod
    def from_dict(_dict: dict) -> TrainingSetup:
        return TrainingSetup(
            _dict["racer_id"],
            [TrainingRunSetup.from_dict(s) for s in _dict["setups"]],
            _dict["save_results"],
            _dict["initial_temperature"],
            _dict["cooling_rate"],
            _dict["convergence_threshold"],
            _dict["convergence_iterations"],
            _dict["n_iterations"],
            _dict["progress_objective"],
            _dict["time_objective"],
            _dict["max_training_time"],
            _dict["greedy"],
            MutationSetup.from_dict(_dict["mutation_setup"]),
        )
    
    def to_dict(self) -> dict:
        return {
            "racer_id": self.racer_id,
            "setups": [s.to_dict() for s in self.setups],
            "save_results": self.save_results,
            "initial_temperature": self.initial_temperature,
            "cooling_rate": self.cooling_rate,
            "convergence_threshold": self.convergence_threshold,
            "convergence_iterations": self.convergence_iterations,
            "n_iterations": self.n_iterations,
            "progress_objective": self.progress_objective,
            "time_objective": self.time_objective,
            "max_training_time": self.max_training_time,
            "greedy": self.greedy,
            "mutation_setup": self.mutation_setup.to_dict(),
        }


class Training():

    training_id: str
    setup: TrainingSetup
    run_history: list[list[Run]]
    clone_history: list[str]
    brain_history: list[Brain]
    elapsed_time: float
    end_reason: str

    def __init__(
            self,
            _training_id: str,
            _setup: TrainingSetup,
            _run_history: list[list[Run]],
            _clone_history: list[str],
            _brain_history: list[Brain],
            _elapsed_time: float,
            _end_reason: str,
        ) -> None:
        self.training_id = _training_id
        self.setup = _setup
        self.run_history = _run_history
        self.clone_history = _clone_history
        self.brain_history = _brain_history
        self.elapsed_time = _elapsed_time
        self.end_reason = _end_reason
    
    @staticmethod
    def from_dict(_dict: dict) -> Training:
        return Training(
            _dict["training_id"],
            TrainingSetup.from_dict(_dict["setup"]),
            [[Run.from_dict(r) for r in it] for it in _dict["run_history"]],
            _dict["clone_history"],
            [Brain.from_dict(b) for b in _dict["brain_history"]],
            _dict["elapsed_time"],
            _dict["end_reason"],
        )

    def get_setup_stat_history(
            self,
            setup_idx: int,
        ) -> list[RunStats]:
        stats: list[RunStats] = []
        first_stat: RunStats|None = self.run_history[0][setup_idx].get_stats_from_racer(self.setup.racer_id)
        if first_stat is not None:
            stats.append(first_stat)
        for i in range(len(self.run_history)):
            stat: RunStats|None = self.run_history[i][setup_idx].get_stats_from_racer(self.clone_history[i])
            if stat is not None:
                stats.append(stat)
        return stats
    
    def create_setup_trace_name(
            self,
            setup_idx: int,
        ) -> str:
        setup: TrainingRunSetup = self.setup.setups[setup_idx]
        track: Track|None = Track.load(setup.track_id)
        trace_name: str = ""
        if track is not None:
            trace_name = track.name
            if setup.run_setup.mirrored:
                trace_name += " (Espelhado)"
        return trace_name

    def generate_setup_progress_evolution_traces(
            self,
            setup_idx: int,
        ) -> list[dict]:
        trace_name: str = self.create_setup_trace_name(setup_idx)
        stats: list[RunStats] = self.get_setup_stat_history(setup_idx)
        progress: np.ndarray = np.array([s.max_progress for s in stats])
        trace_mode: str = "lines+markers" if len(stats) < 30 else "lines"
        traces: list[dict] = [
            {
                "type": "scatter",
                "mode": trace_mode,
                "name": trace_name,
                "x": [i for i in range(len(progress))],
                "y": progress,
            }
        ]
        return traces

    def generate_setup_time_evolution_traces(
            self,
            setup_idx: int,
        ) -> list[dict]:
        trace_name: str = self.create_setup_trace_name(setup_idx)
        stats: list[RunStats] = self.get_setup_stat_history(setup_idx)
        time: np.ndarray = np.array([s.time if s.finished else None for s in stats])
        trace_mode: str = "lines+markers" if len(stats) < 30 else "lines"
        traces: list[dict] = [
            {
                "type": "scatter",
                "mode": trace_mode,
                "name": trace_name,
                "x": [i for i in range(len(time))],
                "y": time,
            }
        ]
        return traces

    def generate_progress_traces(
            self,
            setup_idx: int,
            iteration: int = 0,
        ) -> list[dict]:
        if iteration == 0:
            return self.run_history[0][setup_idx].generate_racer_progress_traces(self.setup.racer_id)
        else:
            return self.run_history[iteration-1][setup_idx].generate_racer_progress_traces(self.clone_history[iteration-1])

    def generate_history_traces(
            self,
            setup_idx: int,
            iteration: int = 0,
        ) -> list[dict]:
        if iteration == 0:
            return self.run_history[0][setup_idx].generate_racer_history_traces(self.setup.racer_id)
        else:
            return self.run_history[iteration-1][setup_idx].generate_racer_history_traces(self.clone_history[iteration-1])


class TrainingEntry():

    training_id: str
    status: str
    created_at: datetime
    finished_at: datetime|None = None

    def __init__(
            self,
            _training_id: str,
            _status: str,
            _created_at: datetime,
            _finished_at: datetime|None = None,
        ) -> None:
        self.training_id = _training_id
        self.status = _status
        self.created_at = _created_at
        self.finished_at = _finished_at
    
    @staticmethod
    def from_dict(_dict: dict) -> TrainingEntry:
        _finished_at: datetime|None = None
        if _dict["finished_at"] is not None:
            _finished_at = datetime.strptime(_dict["finished_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
        return TrainingEntry(
            _dict["training_id"],
            _dict["status"],
            datetime.strptime(_dict["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z"),
            _finished_at,
        )