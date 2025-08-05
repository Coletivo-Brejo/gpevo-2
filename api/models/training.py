from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from .brain import Brain, MutationSetup
from .run import RunSetup


class TrainingRunSetup(BaseModel):
    track_id: str
    run_setup: RunSetup

class TrainingSetup(BaseModel):
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

class Training(BaseModel):
    training_id: str
    setup: TrainingSetup
    iteration: int
    convergence_iteration: int
    temperature: float
    run_id_history: list[list[str]]
    clone_history: list[str]
    brain_history: list[Brain]
    elapsed_time: float
    end_reason: str

class TrainingEntry(BaseModel):
    training_id: str
    status: str
    created_at: datetime
    finished_at: Optional[datetime] = None