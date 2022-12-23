import random
import sys
import time
from enum import Enum
from queue import Queue

import pygame as pg
from pygame.locals import *


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class Config:
    background_color = pg.Color("#5C5C5C")  # the background color
    head_color: pg.Color = pg.Color("#FFC645")  # the color of snake head
    tail_color: pg.Color = pg.Color("#FFDF96")  # the color of snake tail(body)
    food_color: pg.Color = pg.Color("#93FFAB")  # the color of default food
    line_color: pg.Color = pg.Color("#FFFFFF")  # the color of auxiliary line
    map_max_width: int = 400  # the maximum value of the border width (Cartesian coordinate)
    map_max_height: int = 400  # the maximum value of the height width
    grid_width: int = 20  # the value of the grid width (rectangle)
    grid_max_width: int = map_max_width // grid_width  # Cartesian coordinate which unit equals to grid_with
    grid_max_height: int = map_max_height // grid_width

def get_map_size() -> (int, int):
    return Config.map_max_width, Config.map_max_height

def get_grid_size() -> (int, int):
    return Config.grid_max_width, Config.grid_max_height

def random_position():
    random_x = random.randint(0, Config.grid_max_height - 1) * Config.grid_width
    random_y = random.randint(0, Config.grid_max_width - 1) * Config.grid_width
    return Position(random_x, random_y)


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.grid_x = self.x // Config.grid_width
        self.grid_y = self.y // Config.grid_width

    def get_pos(self) -> tuple:
        return self.x, self.y,

    def get_gird_pos(self) -> tuple:
        return self.grid_x, self.grid_y,

    def update_pos(self, x: int, y: int):
        self.x = x
        self.y = y
        self.grid_x = self.x // Config.grid_width
        self.grid_y = self.y // Config.grid_width

    def get_all_orientation(self) -> dict:
        b_x, b_y = get_map_size()
        mid_x, mid_y = self.x + Config.grid_width // 2, self.y + Config.grid_width // 2
        distance = lambda t: (t[0] ** 2 + t[1] ** 2) ** 0.5
        orientation = {
            "E": abs(mid_x - b_x), "S": abs(mid_y - b_y), "N": mid_y, "W": mid_x
        }
        orientation["EN"] = distance((orientation["E"], orientation["N"]))  # 東北
        orientation["WN"] = distance((orientation["W"], orientation["N"]))  # 西北
        orientation["ES"] = distance((orientation["E"], orientation["S"]))  # 東南
        orientation["WS"] = distance((orientation["W"], orientation["S"]))  # 西南
        return orientation

    def __repr__(self):
        return f"position (x: {self.x},y: {self.y})"


class Food:
    def __init__(self):
        self.food_type = "default"  # for skilled food
        self.pos = random_position()

    @classmethod
    def new_food(cls):
        f = Food()
        print(f"Generate new food: {f}")
        return f

    def __repr__(self):
        return f"Food: {id(self)} at {self.pos}"

    def draw(self, screen):
        rect = pg.Rect(*self.pos.get_pos(), Config.grid_width, Config.grid_width)
        pg.draw.rect(screen, Config.food_color, rect)


class Snake:
    def __init__(self):
        self.head_pos: Position = random_position()
        self.bodies: [Position] = [self.head_pos]
        self.last_direction = None
        self.directions: Queue = Queue()
        self.directions.put(Direction.LEFT if self.head_pos.x > Config.map_max_height // 2 else Direction.RIGHT)
        print(f"snake generate at {self.head_pos}")

    def moving(self):
        while not self.directions.empty():
            direction = self.directions.get()
            if direction == Direction.UP and self.last_direction != Direction.DOWN:
                self.head_pos = Position(self.bodies[0].x, self.bodies[0].y - Config.grid_width)

            elif direction == Direction.DOWN and self.last_direction != Direction.UP:
                self.head_pos = Position(self.bodies[0].x, self.bodies[0].y + Config.grid_width)

            elif direction == Direction.LEFT and self.last_direction != Direction.RIGHT:
                self.head_pos = Position(self.bodies[0].x - Config.grid_width, self.bodies[0].y)

            elif direction == Direction.RIGHT and self.last_direction != Direction.LEFT:
                self.head_pos = Position(self.bodies[0].x + Config.grid_width, self.bodies[0].y)
            else: continue
            self.bodies.insert(0, self.head_pos)
            self.bodies.pop(len(self.bodies) - 1)
            self.last_direction = direction
            # print(self.head_pos.get_all_orientation())

    def draw(self, screen, draw_line=True):
        # draw head (with different color)
        h_x, h_y = self.head_pos.get_pos()
        head_rect = pg.Rect(h_x, h_y, Config.grid_width, Config.grid_width)
        pg.draw.rect(screen, Config.head_color, head_rect)
        # draw tail (with different color)
        for tail_pos in self.bodies[1:]:
            t_x, t_y = tail_pos.get_pos()
            tail_rect = pg.Rect(t_x, t_y, Config.grid_width, Config.grid_width)
            pg.draw.rect(screen, Config.tail_color, tail_rect)
        # draw 8 direction line
        if draw_line:
            orientation: dict = self.head_pos.get_all_orientation()
            b_x, b_y = get_map_size()
            snake_mid_point = mid_x, mid_y = self.head_pos.x + Config.grid_width // 2, self.head_pos.y + Config.grid_width // 2
            points = [(0, mid_y), (b_x, mid_y), (mid_x, 0), (mid_x, b_y), (0, 0), (b_x, 0), (0, b_y), (b_x, b_y)]
            for point in points:
                pg.draw.line(screen, Config.line_color, snake_mid_point, point, 2)

    def draw_food_line(self, screen, food):
        food_point = food.pos.get_pos()
        food_point = (food_point[0] + Config.grid_width // 2, food_point[1] + Config.grid_width // 2)
        snake_mid_point = self.head_pos.x + Config.grid_width // 2, self.head_pos.y + Config.grid_width // 2
        pg.draw.line(screen, Config.food_color, snake_mid_point, food_point, 2)

    def check_wall_collision(self):
        x, y = self.head_pos.get_pos()
        return x < 0 or x >= Config.map_max_width or y < 0 or y >= Config.map_max_height

    def check_body_collision(self):
        for tail_pos in self.bodies[1:]:
            if self.head_pos.get_pos() == tail_pos.get_pos():
                return True
        return False

    def check_food_collision(self, food: Food):
        for body in self.bodies:
            if body.get_pos() == food.pos.get_pos():
                return True
        return False

    def add_body(self, pos: Position):
        self.bodies.append(pos)


class Game:
    def __init__(self, mode: str= "default"):
        self.snake: Snake|None = None
        self.foods: list[Food] = []
        self.game_over: bool = False
        self.score = 0
        self.background = None
        self.screen = None
        self.mode = mode
        self.clock = None


    def game_init(self):
        self.snake: Snake = Snake()
        self.foods: list[Food] = [Food.new_food()]
        self.game_over: bool = False
        self.score = 0
        if self.mode == "default":
            self.clock = pg.time.Clock()
            self.background = pg.display.set_mode(get_map_size())
        self.screen = pg.Surface(get_map_size())
        self.screen.fill(Config.background_color)

    def update_food(self):
        for food in self.foods[:]:
            if self.snake.check_food_collision(food):
                self.score += 1
                self.snake.add_body(food.pos)
                self.foods.remove(food)
                new_food = Food.new_food()
                while self.snake.check_food_collision(new_food):
                    new_food = Food.new_food()
                self.foods.append(new_food)
        for food in self.foods:
            food.draw(self.screen)

    def update_snake(self):
        if self.snake.directions.empty():
            self.snake.directions.put(self.snake.last_direction)
        self.snake.moving()
        self.snake.draw(self.screen)
        self.snake.draw_food_line(self.screen, self.foods[0])

    def draw_line(self):
        for index in range(Config.grid_max_width):
            v_start_pos: tuple = (index * Config.grid_width, 0)
            v_end_pos: tuple = (index * Config.grid_width, Config.map_max_height)
            pg.draw.line(self.screen, Config.line_color, v_start_pos, v_end_pos, 1)

        for index in range(Config.grid_max_height):
            h_start_pos: tuple = (0, index * Config.grid_width)
            h_send_pos: tuple = (Config.map_max_width, index * Config.grid_width)
            pg.draw.line(self.screen, Config.line_color, h_start_pos, h_send_pos, 1)

    def update_window(self):
        self.screen.fill(Config.background_color)
        # self.draw_line()
        self.update_food()
        self.update_snake()
        if self.mode == "default":
            self.background.blit(self.screen, (0, 0))
        return self.screen

    def get_screen(self):
        return self.screen

    def update_snake_direction(self, direction: Direction):
        self.snake.directions.put(direction)

    def get_score(self):
        return self.score
    def run(self):
        self.game_init()
        while not self.game_over:
            self.clock.tick(10)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.type == K_ESCAPE:
                        sys.exit()
                    elif not self.game_over:
                        if event.key == K_RIGHT:
                            self.update_snake_direction(Direction.RIGHT)
                        if event.key == K_LEFT:
                            self.update_snake_direction(Direction.LEFT)
                        if event.key == K_UP:
                            self.update_snake_direction(Direction.UP)
                        if event.key == K_DOWN:
                            self.update_snake_direction(Direction.DOWN)

            self.update_window()
            self.game_over = self.snake.check_wall_collision() or self.snake.check_body_collision()
            pg.display.flip()

        return self.game_over


def main():
    pg.init()
    pg.display.set_caption("Snake")
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
