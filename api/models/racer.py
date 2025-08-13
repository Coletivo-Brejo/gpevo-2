from pydantic import BaseModel
from typing import Optional

from .brain import Brain
from .models import Ship


class Racer(BaseModel):
    racer_id: str
    name: str
    brain: Brain
    ship: Ship
    brain_version: Optional[int] = 0