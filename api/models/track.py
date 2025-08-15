from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel

from .models import Point


class TrackSegment(BaseModel):
    length: float
    curvature: float
    l_wall_dist: float
    l_wall_curv: float
    r_wall_dist: float
    r_wall_curv: float

class Track(BaseModel):
    track_id: str
    name: str
    segments: list[TrackSegment]
    loops: bool
    core: list[Point]
    l_wall: list[Point]
    r_wall: list[Point]
    length: float

class LeaderboardEntry(BaseModel):
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

    def performed_better(self, other: LeaderboardEntry) -> bool:
        return self.progress > other.progress or (self.finished and other.finished and self.time < other.time)

    def is_comparable(self, other: LeaderboardEntry) -> bool:
        return self.track_id == other.track_id and self.mirrored == other.mirrored and self.laps == other.laps

class TrackLeaderboard(BaseModel):
    track_id: str
    latest_entries: list[LeaderboardEntry]
    best_entries: list[LeaderboardEntry]