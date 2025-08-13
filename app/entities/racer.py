from __future__ import annotations

from .brain import Brain
from .ship import Ship
from utils.proxy import load_resource_dict


class Racer():

    racer_id: str
    name: str
    brain: Brain
    ship: Ship
    brain_version: int

    def __init__(
            self,
            _racer_id: str,
            _name: str,
            _brain: Brain,
            _ship: Ship,
            _brain_version: int,
        ) -> None:
        self.racer_id = _racer_id
        self.name = _name
        self.brain = _brain
        self.ship = _ship
        self.brain_version = _brain_version
    
    @staticmethod
    def from_dict(_dict: dict) -> Racer:
        return Racer(
            _dict["racer_id"],
            _dict["name"],
            Brain.from_dict(_dict["brain"]),
            Ship.from_dict(_dict["ship"]),
            _dict["brain_version"],
        )

    @staticmethod
    def load(racer_id: str) -> Racer|None:
        racer_dict: dict|None = load_resource_dict("/racers", racer_id)
        if racer_dict is not None:
            racer: Racer = Racer.from_dict(racer_dict)
            return racer
        else:
            return None