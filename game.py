import sys
from typing import Union, Tuple
import pygame as pg
from pygame.locals import *
from setting import GameConfig
from snake import Snake
from misc import *

class Food:
    def __init__(self):
        self.food_type = "default"  # for skilled food
        self.pos = random_position()

    @classmethod
    def new_food(cls):
        f = Food()
        return f

    def __repr__(self):
        return f"Food: {id(self)} at {self.pos}"

    def draw(self, screen):
        rect = pg.Rect(*self.pos.get_point(), GameConfig.grid_width, GameConfig.grid_width)
        pg.draw.rect(screen, GameConfig.food_color, rect)

class Game:
    def __init__(self, mode: str= "default"):
        self.snake: Snake|None = None
        self.fruit: Food|None = None
        self.game_over: bool = False
        self.score = 0
        self.background = None
        self.screen = None
        self.mode = mode
        self.clock = None


    def game_init(self):
        self.snake: Snake = Snake()
        self.fruit = Food.new_food()
        self.game_over: bool = False
        self.score = 0
        if self.mode == "default":
            self.clock = pg.time.Clock()
            self.background = pg.display.set_mode(get_map_size())
        self.screen = pg.Surface(get_map_size())
        self.screen.fill(GameConfig.background_color)

    def update_food(self):
        if self.snake.check_food_collision(self.fruit):
            self.score += 1
            self.snake.add_body(self.fruit.pos)
            new_food = Food.new_food()
            while self.snake.check_food_collision(new_food):
                new_food = Food.new_food()
            self.fruit = new_food

        self.fruit.draw(self.screen)

    def update_snake(self):
        # if self.snake.directions.empty():
        #     self.snake.directions.put(self.snake.last_direction)
        self.snake.moving()
        self.snake.draw(self.screen)
        self.snake.draw_food_line(self.screen, self.fruit)
        print(self.snake.get_feature(self.fruit))

    def draw_line(self):
        for index in range(GameConfig.grid_max_width):
            v_start_pos: tuple = (index * GameConfig.grid_width, 0)
            v_end_pos: tuple = (index * GameConfig.grid_width, GameConfig.map_max_height)
            pg.draw.line(self.screen, GameConfig.line_color, v_start_pos, v_end_pos, 1)

        for index in range(GameConfig.grid_max_height):
            h_start_pos: tuple = (0, index * GameConfig.grid_width)
            h_send_pos: tuple = (GameConfig.map_max_width, index * GameConfig.grid_width)
            pg.draw.line(self.screen, GameConfig.line_color, h_start_pos, h_send_pos, 1)

    def update_window(self):
        self.screen.fill(GameConfig.background_color)
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

if __name__ == "__main__":
    main()