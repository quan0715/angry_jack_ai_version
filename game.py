from __future__ import annotations

from typing import Optional

import pygame as pg

from misc import *
from snake import Snake


class Game:
    def __init__(self):
        self.snake: Optional[Snake] = None
        self.background = None
        self.screen = None

    def game_init(self, snake: Snake):
        self.snake = snake
        self.screen = pg.Surface(get_map_size())
        self.screen.fill(GameConfig.background_color)

    def update_snake(self):
        self.snake.move()
        self.snake.update()

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
        self.snake.draw(self.screen)
        return self.screen

    def get_screen(self):
        return self.screen
