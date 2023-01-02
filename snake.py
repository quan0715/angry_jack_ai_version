from typing import List, Optional
from neural_network import *
from misc import *
from queue import Queue
from genetic_algorithm.individual import Individual
import numpy as np
import pygame as pg
import random
import pickle


class Food:
    def __init__(self, pos: Point):
        self.food_type = "default"  # for skilled food
        self.pos = pos

    def __repr__(self):
        return f"Food: {id(self)} at {self.pos}"

    def draw(self, screen):
        rect = pg.Rect(*(grid_to_coordinate(self.pos).get_point()), GameConfig.grid_width, GameConfig.grid_width)
        pg.draw.rect(screen, GameConfig.food_color, rect)


class Snake(Individual):
    def __init__(self, network: Optional[FFN] = None):
        super().__init__()
        self.head_pos: Point = random_grid_position()
        self.bodies: List[Point] = [self.head_pos]
        self.last_direction = None
        self.tail_direction = None
        self.directions = Queue()

        x, y = grid_to_coordinate(self.head_pos).get_point()

        possible_initial_directions = [Direction.LEFT if x > GameConfig.map_max_height // 2 else Direction.RIGHT,
                                       Direction.UP if y > GameConfig.map_max_width // 2 else Direction.DOWN]
        self.initial_direction = random.choice(possible_initial_directions)
        self.directions.put(self.initial_direction)

        for _ in range(GameConfig.snake_init_length):
            opposite_direction = direction_map[self.initial_direction]['check']
            offset_x = direction_map[opposite_direction]['x_added']
            offset_y = direction_map[opposite_direction]['y_added']
            self.add_body(Point(self.bodies[-1].x + offset_x, self.bodies[-1].y + offset_y))

        self.food = None
        self.is_alive = True
        self.win = False

        # genetic algorithm stuff
        self.score = 0  # Number of apples snake gets
        self.network = network
        if self.network is None:
            self.network = create_default_model()
        self._fitness = 0
        self._frames = 0
        self._frames_since_last_food = 0

        self.generate_food()

    def respawn(self):
        self.is_alive = True
        self.win = False
        self.head_pos: Point = random_grid_position()
        self.bodies: List[Point] = [self.head_pos]
        self.last_direction = None
        self.tail_direction = None
        self.directions = Queue()

        x, y = grid_to_coordinate(self.head_pos).get_point()

        possible_initial_directions = [Direction.LEFT if x > GameConfig.map_max_height // 2 else Direction.RIGHT,
                                       Direction.UP if y > GameConfig.map_max_width // 2 else Direction.DOWN]
        self.initial_direction = random.choice(possible_initial_directions)
        self.directions.put(self.initial_direction)

        for _ in range(GameConfig.snake_init_length):
            opposite_direction = direction_map[self.initial_direction]['check']
            offset_x = direction_map[opposite_direction]['x_added']
            offset_y = direction_map[opposite_direction]['y_added']
            self.add_body(Point(self.bodies[-1].x + offset_x, self.bodies[-1].y + offset_y))

        self.score = 0
        self._fitness = 0
        self._frames = 0
        self._frames_since_last_food = 0

        self.generate_food()

    def generate_food(self):
        # Find all possible points where the snake is not currently
        possibilities = [Point(x, y) for x in range(GameConfig.grid_max_width)
                         for y in range(GameConfig.grid_max_height)
                         if Point(x, y) not in self.bodies]
        if possibilities:
            loc = random.choice(possibilities)
            self.food = Food(loc)
            return True
        return False

    def look_in_direction(self, direction):
        self.directions.put(direction)

    def update(self):
        self._frames += 1
        self._frames_since_last_food += 1
        if self._frames_since_last_food > 100:
            self.is_alive = False
            return

        if self.check_food_collision():
            self.score += 1
            self._frames_since_last_food = 0
            self.add_body(self.food.pos)

            if not self.generate_food():
                self.win = True
                return
        elif self.check_wall_collision() or self.check_body_collision():
            self.is_alive = False
            return
        # print(self.get_feature())
        direction = get_direction(self.network, self.get_feature())
        self.look_in_direction(direction)

    def move(self):
        if not self.is_alive: return
        move_flag = False
        while not self.directions.empty() and not move_flag:
            direction = self.directions.get()
            for d, d_t in direction_map.items():
                if direction == d and self.last_direction != d_t['check']:
                    self.head_pos = Point(
                        self.bodies[0].x + d_t['x_added'],
                        self.bodies[0].y + d_t['y_added']
                    )
                    self.bodies.insert(0, self.head_pos)
                    self.bodies.pop(len(self.bodies) - 1)
                    self.last_direction = direction
                    move_flag = True
                    break
        if not move_flag:
            self.head_pos = Point(
                self.bodies[0].x + direction_map[self.last_direction]['x_added'],
                self.bodies[0].y + direction_map[self.last_direction]['y_added']
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
        h_x, h_y = grid_to_coordinate(self.head_pos).get_point()
        head_rect = pg.Rect(h_x, h_y, GameConfig.grid_width, GameConfig.grid_width)
        pg.draw.rect(screen, GameConfig.head_color, head_rect)
        # draw tail (with different color)
        for tail_pos in self.bodies[1:]:
            t_x, t_y = grid_to_coordinate(tail_pos).get_point()
            tail_rect = pg.Rect(t_x, t_y, GameConfig.grid_width, GameConfig.grid_width)
            pg.draw.rect(screen, GameConfig.tail_color, tail_rect)
        # draw 8 direction line
        if draw_line:
            g_w = GameConfig.grid_width
            head_pos_c = grid_to_coordinate(self.head_pos)
            mid_x, mid_y = head_pos_c.x + g_w // 2, head_pos_c.y + g_w // 2
            for b in eight_vision.values():
                init_point = Point(mid_x, mid_y)
                while not init_point.point_in_wall():
                    init_point.x += b['x_added']
                    init_point.y += b['y_added']
                pg.draw.line(screen, GameConfig.line_color, (mid_x, mid_y), init_point.get_point(), 2)

        self.food.draw(screen)

    def check_wall_collision(self):
        x, y = grid_to_coordinate(self.head_pos).get_point()
        return x < 0 or x >= GameConfig.map_max_width or y < 0 or y >= GameConfig.map_max_height

    def check_body_collision(self):
        return self.head_pos in self.bodies[1:]

    def check_food_collision(self):
        return self.food.pos in self.bodies

    def is_alive(self):
        return not self.check_wall_collision() and not self.check_body_collision()

    def add_body(self, pos: Point):
        self.bodies.append(pos)

    def get_feature(self) -> np.array:
        feature_list = []
        # 8 vision
        snake_point = self.head_pos
        for direction, vision in eight_vision.items():
            dist_to_apple = np.inf
            dist_to_self = np.inf

            distance = 1.0
            total_distance = 0.0

            cur = Point(*snake_point.get_point())

            cur.x += vision['x_added']
            cur.y += vision['y_added']
            total_distance += distance
            body_found = False
            food_found = False
            while not grid_to_coordinate(cur).point_in_wall():
                if not body_found and cur.point_in_body(self):
                    dist_to_self = total_distance
                    body_found = True
                if not food_found and cur.point_in_food(self.food):
                    dist_to_apple = total_distance
                    food_found = True

                cur.x += vision['x_added']
                cur.y += vision['y_added']
                total_distance += distance

            dist_to_wall = 1.0 / total_distance

            if GameConfig.vision_type == 'binary':
                dist_to_apple = 1.0 if dist_to_apple != np.inf else 0.0
                dist_to_self = 1.0 if dist_to_self != np.inf else 0.0

            elif GameConfig.vision_type == 'distance':
                dist_to_apple = 1.0 / dist_to_apple
                dist_to_self = 1.0 / dist_to_self

            feature_list.extend([dist_to_wall, dist_to_apple, dist_to_self])

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

    @staticmethod
    def load(file_name):
        with open(file_name, 'rb') as f:
            network = pickle.load(f)
            return Snake(network)

    def save(self):
        with open(f'best_snake.pkl', 'wb') as f:
            pickle.dump(self.network, f)
