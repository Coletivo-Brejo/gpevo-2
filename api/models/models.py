from pydantic import BaseModel


class Point(BaseModel):
    x: float
    y: float

class Thruster(BaseModel):
    power: float
    texture: str
    position: Point
    rotation: float

class SensorSet(BaseModel):
    amount: int
    aperture: float
    reach: float
    texture: str
    position: Point
    rotation: float

class Ship(BaseModel):
    ship_id: str
    name: str
    mass: float
    chassis_texture: str
    chassis_collision: list[Point]
    thrusters: list[Thruster]
    sensors: list[SensorSet]