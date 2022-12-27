from typing import List, Optional
from neural_network import FFN
from misc import *
from queue import Queue
from genetic_algorithm.individual import Individual
import numpy as np
import pygame as pg


class Snake(Individual):
    def __init__(self):
        super().__init__()
        self.head_pos: Point = random_position()
        self.bodies: List[Point] = [self.head_pos]
        self.last_direction = None
        self.tail_direction = None
        self.directions: Queue = Queue()
        self.directions.put(Direction.LEFT if self.head_pos.x > GameConfig.map_max_height // 2 else Direction.RIGHT)

        # genetic algorithm stuff
        self.score = 0  # Number of apples snake gets
        self.network: Optional[FFN] = None
        self._fitness = 0
        self._frames = 0

        print(f"snake generate at {self.head_pos}")

    def moving(self):
        move_flag = False
        while not self.directions.empty() and not move_flag:
            direction = self.directions.get()
            for d, d_t in direction_map.items():
                if direction == d and self.last_direction != d_t['check']:
                    self.head_pos = Point(
                        self.bodies[0].x + GameConfig.grid_width * d_t['x_added'],
                        self.bodies[0].y + GameConfig.grid_width * d_t['y_added']
                    )
                    self.bodies.insert(0, self.head_pos)
                    self.bodies.pop(len(self.bodies) - 1)
                    self.last_direction = direction
                    move_flag = True
                    break
        if not move_flag:
            self.head_pos = Point(
                self.bodies[0].x + GameConfig.grid_width * direction_map[self.last_direction]['x_added'],
                self.bodies[0].y + GameConfig.grid_width * direction_map[self.last_direction]['y_added']
            )
            self.bodies.insert(0, self.head_pos)
            self.bodies.pop(len(self.bodies) - 1)
        # update tail direction
        if len(self.bodies) >= 2:
            diff_x, diff_y = (self.bodies[-1] - self.bodies[-2]).get_point()
            if diff_x == 0 and diff_y < 0:
                self.tail_direction = Direction.DOWN
            elif diff_x == 0 and diff_y > 0:
                self.tail_direction = Direction.UP
            elif diff_y == 0 and diff_x > 0:
                self.tail_direction = Direction.LEFT
            elif diff_y == 0 and diff_x < 0:
                self.tail_direction = Direction.RIGHT
        else:
            self.tail_direction = self.last_direction

    def draw(self, screen, draw_line=True):
        # draw head (with different color)
        h_x, h_y = self.head_pos.get_point()
        head_rect = pg.Rect(h_x, h_y, GameConfig.grid_width, GameConfig.grid_width)
        pg.draw.rect(screen, GameConfig.head_color, head_rect)
        # draw tail (with different color)
        for tail_pos in self.bodies[1:]:
            t_x, t_y = tail_pos.get_point()
            tail_rect = pg.Rect(t_x, t_y, GameConfig.grid_width, GameConfig.grid_width)
            pg.draw.rect(screen, GameConfig.tail_color, tail_rect)
        # draw 8 direction line
        if draw_line:
            # orientation: dict = self.head_pos.get_eight_orientation_distance()
            # b_x, b_y = get_map_size()
            # eight_vision
            g_w = GameConfig.grid_width
            snake_mid_point = mid_x, mid_y = self.head_pos.x + g_w // 2, self.head_pos.y + g_w // 2
            for b in eight_vision.values():
                init_point = Point(mid_x, mid_y)
                while not self._point_in_wall(init_point):
                    init_point.x += b['x_added']
                    init_point.y += b['y_added']
                pg.draw.line(screen, GameConfig.line_color, snake_mid_point, init_point.get_point(), 2)

    def draw_food_line(self, screen, food):
        food_point = food.pos.get_point()
        food_point = (food_point[0] + GameConfig.grid_width // 2, food_point[1] + GameConfig.grid_width // 2)
        snake_mid_point = self.head_pos.x + GameConfig.grid_width // 2, self.head_pos.y + GameConfig.grid_width // 2
        pg.draw.line(screen, GameConfig.food_color, snake_mid_point, food_point, 2)

    def check_wall_collision(self):
        x, y = self.head_pos.get_point()
        return x < 0 or x >= GameConfig.map_max_width or y < 0 or y >= GameConfig.map_max_height

    def check_body_collision(self):
        return self.head_pos in self.bodies[1:]

    def check_food_collision(self, food):
        return food.pos in self.bodies

    def _point_in_wall(self, point: Point) -> bool:
        x, y = point.get_point()
        return x < 0 or x >= GameConfig.map_max_width or y < 0 or y >= GameConfig.map_max_height

    def _point_in_body(self, point: Point) -> bool:
        return point in self.bodies[1:]

    def _point_in_food(self, food, point: Point) -> bool:
        return food.pos == point

    def is_alive(self):
        return not self.check_wall_collision() and not self.check_body_collision()

    def add_body(self, pos: Point):
        self.bodies.append(pos)

    def get_feature(self, fruit) -> np.array:
        feature_list = []
        # 8 vision
        snake_point = self.head_pos
        for direction, vision in eight_vision.items():
            vision_feature = {"self_to_wall": 0, "self_to_food": 0, "self_to_self": 0}
            start_point = Point(*snake_point.get_point())
            while not self._point_in_wall(start_point):
                start_point.x += vision['x_added'] * GameConfig.grid_width
                start_point.y += vision['y_added'] * GameConfig.grid_width
                if self._point_in_body(start_point):
                    vision_feature['self_to_self'] = Point.euclidean_distance(snake_point, start_point)
                if self._point_in_food(fruit, start_point):
                    vision_feature['self_to_food'] = Point.euclidean_distance(snake_point, start_point)

            vision_feature['self_to_wall'] = Point.euclidean_distance(snake_point, start_point)
            feature_list.extend(list(vision_feature.values()))

        # head direction in one hot encoding
        head_direction = [0, 0, 0, 0]
        head_direction[direction_map[self.last_direction]['index']] = 1
        feature_list.extend(head_direction)

        # tail direction in one hot encoding
        tail_direction = [0, 0, 0, 0]
        tail_direction[direction_map[self.tail_direction]['index']] = 1
        # print(self.last_direction, self.tail_direction)
        feature_list.extend(tail_direction)
        feature = np.array(feature_list)
        # print(feature)
        return feature

    @property
    def fitness(self):
        return self._fitness

    def calculate_fitness(self):
        # Give positive minimum fitness for roulette wheel selection
        self._fitness = self._frames + ((2 ** self.score) + (self.score ** 2.1) * 500) - (
                ((.25 * self._frames) ** 1.3) * (self.score ** 1.2))
        self._fitness = max(self._fitness, .1)
