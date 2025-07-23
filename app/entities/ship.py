from __future__ import annotations

from .point import Point


class Thruster():

    power: float
    texture: str
    position: Point
    rotation: float

    def __init__(
            self,
            _power: float,
            _texture: str,
            _position: Point,
            _rotation: float,
        ) -> None:
        self.power = _power
        self.texture = _texture
        self.position = _position
        self.rotation = _rotation
    
    @staticmethod
    def from_dict(_dict: dict) -> Thruster:
        return Thruster(
            _dict["power"],
            _dict["texture"],
            Point.from_dict(_dict["position"]),
            _dict["rotation"],
        )
    

class SensorSet():

    amount: int
    aperture: float
    reach: float
    texture: str
    position: Point
    rotation: float

    def __init__(
            self,
            _amount: int,
            _aperture: float,
            _reach: float,
            _texture: str,
            _position: Point,
            _rotation: float,
        ) -> None:
        self.amount = _amount
        self.aperture = _aperture
        self.reach = _reach
        self.texture = _texture
        self.position = _position
        self.rotation = _rotation
    
    @staticmethod
    def from_dict(_dict: dict) -> SensorSet:
        return SensorSet(
            _dict["amount"],
            _dict["aperture"],
            _dict["reach"],
            _dict["texture"],
            Point.from_dict(_dict["position"]),
            _dict["rotation"],
        )


class Ship():

    ship_id: str
    name: str
    mass: float
    chassis_texture: str
    chassis_collision: list[Point]
    thrusters: list[Thruster]
    sensors: list[SensorSet]

    def __init__(
            self,
            _ship_id: str,
            _name: str,
            _mass: float,
            _chassis_texture: str,
            _chassis_collision: list[Point],
            _thrusters: list[Thruster],
            _sensors: list[SensorSet],
        ) -> None:
        self.ship_id = _ship_id
        self.name = _name
        self.mass = _mass
        self.chassis_texture = _chassis_texture
        self.chassis_collision = _chassis_collision
        self.thrusters = _thrusters
        self.sensors = _sensors
    
    @staticmethod
    def from_dict(_dict: dict) -> Ship:
        return Ship(
            _dict["ship_id"],
            _dict["name"],
            _dict["mass"],
            _dict["chassis_texture"],
            [Point.from_dict(p) for p in _dict["chassis_collision"]],
            [Thruster.from_dict(t) for t in _dict["thrusters"]],
            [SensorSet.from_dict(s) for s in _dict["sensors"]],
        )
