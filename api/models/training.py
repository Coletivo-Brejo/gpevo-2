from pydantic import BaseModel

from .brain import MutationSetup
from .models import Run, RunSetup


class TrainingRunSetup(BaseModel):
    track_id: str
    run_setup: RunSetup

class Training(BaseModel):
    training_id: str
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
    run_history: list[list[Run]]
    clone_history: list[str]
    elapsed_time: float
    end_reason: str