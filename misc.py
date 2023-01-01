from setting import GameConfig
from typing import Union, Tuple
import random
from enum import IntEnum


def get_map_size() -> Tuple[int, int]:
    return GameConfig.map_max_width, GameConfig.map_max_height


def get_grid_size() -> Tuple[int, int]:
    return GameConfig.grid_max_width, GameConfig.grid_max_height


def random_position():
    random_x = random.randint(0, GameConfig.grid_max_height - 1) * GameConfig.grid_width
    random_y = random.randint(0, GameConfig.grid_max_width - 1) * GameConfig.grid_width
    return Point(random_x, random_y)


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.grid_x = self.x // GameConfig.grid_width
        self.grid_y = self.y // GameConfig.grid_width

    def get_point(self) -> tuple:
        return self.x, self.y,

    def update_point(self, x: int, y: int):
        self.x = x
        self.y = y
        self.grid_x = self.x // GameConfig.grid_width
        self.grid_y = self.y // GameConfig.grid_width

    @classmethod
    def euclidean_distance(cls, point1, point2):
        if isinstance(point1, tuple):
            point1 = Point(point1[0], point1[1])
        if isinstance(point2, tuple):
            point1 = Point(point2[0], point2[1])
        return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5

    def __eq__(self, other: Union['Point', Tuple[int, int]]) -> bool:
        if isinstance(other, tuple) and len(other) == 2:
            return other[0] == self.x and other[1] == self.y
        elif isinstance(other, Point) and self.x == other.x and self.y == other.y:
            return True
        return False

    def __sub__(self, other: Union["Point", Tuple[int, int]]) -> "Point":
        if isinstance(other, tuple) and len(other) == 2:
            diff_x = self.x - other[0]
            diff_y = self.y - other[1]
            return Point(diff_x, diff_y)
        elif isinstance(other, Point):
            diff_x = self.x - other.x
            diff_y = self.y - other.y
            return Point(diff_x, diff_y)

    def __repr__(self):
        return f"position (x: {self.x},y: {self.y})"


class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


direction_map = {
    Direction.UP: {'check': Direction.DOWN, "x_added": 0, "y_added": -1, "index": 0},
    Direction.DOWN: {'check': Direction.UP, "x_added": 0, "y_added": 1, "index": 1},
    Direction.LEFT: {'check': Direction.RIGHT, "x_added": -1, "y_added": 0, "index": 2},
    Direction.RIGHT: {'check': Direction.LEFT, "x_added": 1, "y_added": 0, "index": 3}
}

# self.x * c0 + width * c1 , self.y*c2 + height * c3
eight_vision = {
    "E": {"x_added": 1, "y_added": 0},
    "S": {"x_added": 0, "y_added": 1},
    "W": {"x_added": -1, "y_added": 0},
    "N": {"x_added": 0, "y_added": -1},
    "ES": {"x_added": 1, "y_added": 1},
    "EN": {"x_added": 1, "y_added": -1},
    "WS": {"x_added": -1, "y_added": 1},
    "WN": {"x_added": -1, "y_added": -1},
}
