from __future__ import annotations

import sys
from typing import Union, Tuple, Optional
import pygame as pg
from pygame.locals import *
from setting import GameConfig
from snake import Snake
from misc import *


class Game:
    def __init__(self, mode: str = "default"):
        self.snake: Optional[Snake] = None
        self.background = None
        self.screen = None
        self.mode = mode
        self.clock = None

    def game_init(self, snake: Snake):
        self.snake = snake
        if self.mode == "default":
            self.clock = pg.time.Clock()
            self.background = pg.display.set_mode(get_map_size())
        self.screen = pg.Surface(get_map_size())
        self.screen.fill(GameConfig.background_color)

    def update_snake(self):
        self.snake.move()
        self.snake.update()
        self.snake.draw(self.screen)

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
        self.update_snake()
        if self.mode == "default":
            self.background.blit(self.screen, (0, 0))
        return self.screen

    def get_screen(self):
        return self.screen
