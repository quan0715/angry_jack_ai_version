import random
import time
from copy import copy
from queue import Queue
import pygame as pg
from pygame.locals import *
import sys
class Direction:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class GameMap:
    def __init__(self, map_width: int, map_height: int, unit: int):
        self.map_width: int = map_width
        self.map_height: int = map_height
        self.unit: int = unit
        self.grid_width: int = self.map_width // self.unit
        self.grid_height: int = self.map_height // self.unit

    def get_map_size(self) -> (int, int):
        return self.map_width, self.map_height

    def get_grid_size(self)->(int, int):
        return self.grid_width, self.grid_height

class Position:
    game_map: GameMap
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.grid_x = self.x // Position.game_map.unit
        self.grid_y = self.y // Position.game_map.unit
    def get_pos(self) -> tuple:
        return self.x, self.y,
    def get_gird_pos(self) -> tuple:
        return self.grid_x, self.grid_y,

    def update_pos(self, x: int, y: int):
        self.x = x
        self.y = y
        self.grid_x = self.x // Position.game_map.unit
        self.grid_y = self.y // Position.game_map.unit

    @classmethod
    def random_position(cls,):
        random_x = random.randint(0, Position.game_map.grid_width - 1) * cls.game_map.unit
        random_y = random.randint(0, Position.game_map.grid_height - 1) * cls.game_map.unit
        return Position(random_x, random_y)
    @classmethod
    def setting(cls, game_map: GameMap):
        cls.game_map = game_map

    def __repr__(self):
        return f"position (x: {self.x},y: {self.y})"

class Food:
    game_map: GameMap
    def __init__(self):
        self.food_type = "default"  # for skilled food
        self.pos = Position.random_position()

    def be_eaten(self, snake):
        print(f"food {self} is eaten by {snake}")

    @classmethod
    def new_food(cls):
        f = Food()
        print(f"Generate new food: {f}")
        return f

    @classmethod
    def setting(cls, game_map: GameMap):
        cls.game_map: GameMap = game_map

    def __repr__(self):
        return f"Food: {id(self)} at {self.pos}"

    def draw(self, screen):
        pg.draw.rect(screen,(255,0,0),pg.Rect(*self.pos.get_pos(),Food.game_map.unit,Food.game_map.unit))

class Snake:
    game_map: GameMap

    def __init__(self):
        self.head_pos: Position = Position.random_position()
        self.bodies: [Position] = [self.head_pos]
        self.length = len(self)
        self.last_direction = None
        self.directions:Queue = Queue()
        self.directions.put(Direction.LEFT if self.head_pos.x > Snake.game_map.map_width // 2 else Direction.RIGHT)
        self.head_color = pg.Color("#FFC645")
        self.tail_color = pg.Color("#FFDF96")
        print(f"snake generate at {self.head_pos}")

    def __len__(self):
        return len(self.bodies)

    def move_up(self):
        self.head_pos = Position(self.bodies[0].x,self.bodies[0].y-Snake.game_map.unit)
        self.bodies.insert(0,self.head_pos)
        self.bodies.pop(len(self.bodies)-1)
        # for body in self.bodies:
        #     body.update_pos(body.x, body.y - Snake.game_map.unit)
        self.last_direction = Direction.UP
    def move_down(self):
        self.head_pos = Position(self.bodies[0].x,self.bodies[0].y+Snake.game_map.unit)
        self.bodies.insert(0, self.head_pos)
        self.bodies.pop(len(self.bodies)-1)
        self.last_direction = Direction.DOWN

    def move_right(self):
        self.head_pos = Position(self.bodies[0].x+Snake.game_map.unit,self.bodies[0].y)
        self.bodies.insert(0,self.head_pos)
        self.bodies.pop(len(self.bodies)-1)
        self.last_direction = Direction.RIGHT

    def move_left(self):
        self.head_pos = Position(self.bodies[0].x-Snake.game_map.unit,self.bodies[0].y)
        self.bodies.insert(0,self.head_pos)
        self.bodies.pop(len(self.bodies)-1)
        self.last_direction = Direction.LEFT

    def moving(self, screen):
        while not self.directions.empty():
            direction = self.directions.get()
            print(direction, list(self.directions.queue))
            if direction == Direction.UP and self.last_direction != Direction.DOWN:
                self.move_up()
            if direction == Direction.DOWN and self.last_direction != Direction.UP:
                self.move_down()
            if direction == Direction.LEFT and self.last_direction != Direction.RIGHT:
                self.move_left()
            if direction == Direction.RIGHT and self.last_direction != Direction.LEFT:
                self.move_right()
            self.head_pos = self.bodies[0]
            self.draw(screen)
    def draw(self, surface):
        # draw head (with different color)
        # surface.fill(BACKGROUND_COLOR)
        # print(f"draw head at {self.head_pos}")
        h_x, h_y = self.head_pos.get_pos()
        head_rect = pg.Rect(h_x, h_y, Snake.game_map.unit, Snake.game_map.unit)
        pg.draw.rect(surface, self.head_color, head_rect)
        # draw tail (with different color)
        for tail_pos in self.bodies[1:]:
            t_x, t_y = tail_pos.get_pos()
            tail_rect = pg.Rect(t_x, t_y, Snake.game_map.unit, Snake.game_map.unit)
            pg.draw.rect(surface, self.tail_color, tail_rect)

    @classmethod
    def setting(cls, game_map: GameMap):
        cls.game_map: GameMap = game_map

class Game:
    def __init__(self, max_width, max_height, unit):
        self.game_map = GameMap(max_width, max_height, unit)
        Position.setting(self.game_map)
        Snake.setting(self.game_map)
        Food.setting(self.game_map)
        self.snake: Snake = Snake()
        self.foods: list[Food] = []
        self.eaten_foods: list[Food] = []
        self.game_over: bool = False

    def check_status(self):
        pass

    def game_init(self):
        self.foods.append(Food.new_food())

    def touch_wall(self):
        snake_x, snake_y = self.snake.head_pos.get_pos()
        boarder_width , boarder_height = self.game_map.get_map_size()
        if snake_x < 0 or snake_x >= boarder_width or snake_y < 0 or snake_y >= boarder_height:
            return True
        return False

    def touch_body(self):
        for tail_pos in self.snake.bodies[1:]:
            if self.snake.head_pos.get_pos() == tail_pos.get_pos():
                return True
        return False

    def touch_food(self):
        if self.snake.head_pos.get_pos() == self.foods[-1].pos.get_pos():
            self.foods[-1].be_eaten(self.snake)
            self.eaten_foods.append(self.foods[-1])
            print(self.snake.bodies)
            self.foods.append(Food.new_food())
            
    
    def add_tail(self):
        # if len(self.eaten_foods)!=0 and self.snake.bodies[-1] == self.eaten_foods[0]:
        #     self.snake.bodies.append(self.eaten_foods[0].pos)
        #     self.eaten_foods.pop(0)
        for food in self.eaten_foods:
            food_in_body = False
            for body in self.snake.bodies:
                if food.pos.get_pos() == body.get_pos():
                    food_in_body = True
            if not food_in_body:
                self.snake.bodies.append(food.pos)
                self.eaten_foods.pop(0)

    def run(self):
        pg.init()
        self.game_init()
        pg.display.set_caption("Snake")
        screen = pg.display.set_mode(self.game_map.get_map_size())
        background = pg.Surface(screen.get_size())
        background.fill(BACKGROUND_COLOR)
        # font = pg.font.SysFont("Roboto" , 25)
        while not self.game_over:
            time.sleep(0.1)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.type == K_ESCAPE:
                        sys.exit()
                    elif not self.game_over:
                        if event.key == K_RIGHT:
                            self.snake.directions.put(Direction.RIGHT)
                        if event.key == K_LEFT:
                            self.snake.directions.put(Direction.LEFT)
                        if event.key == K_UP:
                            self.snake.directions.put(Direction.UP)
                        if event.key == K_DOWN:
                            self.snake.directions.put(Direction.DOWN)
            background.fill(BACKGROUND_COLOR)
            self.game_over = self.touch_wall() or self.touch_body()
            if self.snake.directions.empty():
                self.snake.directions.put(self.snake.last_direction)
            self.touch_food()
            self.add_tail()
            self.snake.moving(background)
            self.foods[-1].draw(background)
            screen.blit(background, (0, 0))
            pg.display.flip()
def main():
    game = Game(MAX_WIDTH, MAX_HEIGHT, UNIT)
    game.run()

if __name__ == '__main__':
    MAX_WIDTH = 400
    MAX_HEIGHT = 400
    UNIT = 20
    BACKGROUND_COLOR = (0, 0, 0) # black
    main()
