from typing import Optional

import pygame as pg

from misc import *
from snake import Snake
from setting import *


class GameWidget(PygameLayout):
    def __init__(self):
        super().__init__(
            Point(*GUIConfig.snake_game_display_pos),
            GameConfig.map_max_height,
            GameConfig.map_max_width
        )
        self.snake = None

    def game_init(self, snake: Snake):
        self.snake = snake
        # screen = self.get_screen()
        # self.screen.fill(GameConfig.background_color)

    def update_snake(self):
        self.snake.move()
        self.snake.update()

    def draw_line(self, screen):
        for index in range(self.get_width()):
            v_start_pos: tuple = (index * GameConfig.grid_width, 0)
            v_end_pos: tuple = (index * GameConfig.grid_width, GameConfig.map_max_height)
            pg.draw.line(screen, GameConfig.line_color, v_start_pos, v_end_pos, 1)

        for index in range(self.get_height()):
            h_start_pos: tuple = (0, index * GameConfig.grid_width)
            h_send_pos: tuple = (GameConfig.map_max_width, index * GameConfig.grid_width)
            pg.draw.line(screen, GameConfig.line_color, h_start_pos, h_send_pos, 1)

    def draw(self, win):
        screen = self.get_screen()
        screen.fill(GameConfig.background_color)
        # self.draw_line(screen)
        self.snake.draw(screen)
        win.blit(screen, self.get_start_pos().get_point())
