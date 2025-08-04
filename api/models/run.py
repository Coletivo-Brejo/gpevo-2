from pydantic import BaseModel

from .models import Point


class RunStats(BaseModel):
    racer_id: str
    track_id: str
    lap: int
    time: float
    max_progress: float
    finished: bool
    stuck: bool
    time_history: list[float]
    progress_history: list[float]
    position_history: list[Point]

class RunSetup(BaseModel):
    begin_countdown: float
    end_countdown: float
    stuck_timeout: float
    run_timeout: float
    follow_first: bool
    end_on_first_finish: bool
    stat_collection_frequency: float
    mirrored: bool
    laps: int

class Run(BaseModel):
    run_id: str
    track_id: str
    racer_ids: list[str]
    setup: RunSetup
    elapsed_time: float
    end_reason: str
    stats: list[RunStats]