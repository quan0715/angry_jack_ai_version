from misc import *
from queue import Queue
import numpy as np
import pygame as pg

class Snake:
    def __init__(self):
        self.head_pos: Point = random_position()
        self.bodies: list[Point] = [self.head_pos]
        self.last_direction = None
        self.tail_direction = None
        self.directions: Queue = Queue()
        self.directions.put(Direction.LEFT if self.head_pos.x > GameConfig.map_max_height // 2 else Direction.RIGHT)
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
                self.tail_direction = Direction.UP
            elif diff_x == 0 and diff_y > 0:
                self.tail_direction = Direction.DOWN
            elif diff_y == 0 and diff_x > 0:
                self.tail_direction = Direction.RIGHT
            elif diff_y == 0 and diff_x < 0 :
                self.tail_direction = Direction.LEFT
        else: self.tail_direction = self.last_direction
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
            b_x, b_y = get_map_size()
            snake_mid_point = mid_x, mid_y = self.head_pos.x + GameConfig.grid_width // 2, self.head_pos.y + GameConfig.grid_width // 2
            points = [(0, mid_y), (b_x, mid_y), (mid_x, 0), (mid_x, b_y), (0, 0), (b_x, 0), (0, b_y), (b_x, b_y)]
            for point in points:
                pg.draw.line(screen, GameConfig.line_color, snake_mid_point, point, 2)
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
    def add_body(self, pos: Point):
        self.bodies.append(pos)
    def get_feature(self, fruit) -> np.array:
        fruit_pos = fruit.pos.get_point()
        fruit_mid_x, fruit_mid_y = fruit_pos[0] + GameConfig.grid_width // 2, fruit_pos[1] + GameConfig.grid_width // 2
        feature_list = []
        # 8 vision
        eight_vision_distance = self.head_pos.get_eight_orientation_distance()
        for orientation in eight_vision_distance.keys():
            vision_feature = [eight_vision_distance[orientation]]

            # fruit distance
            # part of snake
        head_direction = [0, 0, 0, 0]
        head_direction[direction_map[self.last_direction]['index']] = 1
        feature_list.extend(head_direction)

        tail_direction = [0, 0, 0, 0]
        tail_direction[direction_map[self.tail_direction]['index']] = 1
        feature_list.extend(tail_direction)

        feature = np.array(feature_list)
        return feature