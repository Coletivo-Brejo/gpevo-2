from __future__ import annotations
import numpy as np


class Point():

    x: float
    y: float

    def __init__(
            self,
            _x: float,
            _y: float,
        ) -> None:
        self.x = _x
        self.y = _y
    
    @staticmethod
    def from_dict(_dict: dict) -> Point:
        return Point(_dict["x"], _dict["y"])


class PointList():

    points: list[Point]

    def __init__(
            self,
            _points: list[Point],
        ) -> None:
        self.points = _points
    
    @staticmethod
    def from_list(_list: list[dict]) -> PointList:
        return PointList([Point.from_dict(p) for p in _list])
    
    def xs(self) -> np.ndarray:
        return np.array([p.x for p in self.points])

    def ys(self) -> np.ndarray:
        return np.array([p.y for p in self.points])