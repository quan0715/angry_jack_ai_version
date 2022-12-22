import time
import sys
import pygame as pg
from pygame.locals import *
from game import Game

class GUIConfig:
    window_weight: int = 900
    window_height: int = 600
    snake_game_display_pos: tuple = 480, 20
    background_color = "#000000"


class VisualizeFrame:
    def __init__(self):
        self.background = pg.display.set_mode((GUIConfig.window_weight, GUIConfig.window_height))
        self.background.fill(GUIConfig.background_color)
        self.game = Game("train")
        self.game.game_init()
        self.clock = pg.time.Clock()


    def update_game(self):
        snake_game_screen = self.game.update_window()
        self.background.blit(snake_game_screen, dest=GUIConfig.snake_game_display_pos)

    def build(self):
        pg.init()
        pg.display.set_caption("Module Visualization")
        while True:
            self.clock.tick(10)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()

            self.update_game()
            pg.display.flip()

def main():
    # new_game.run()
    frame = VisualizeFrame()
    frame.build()

if __name__ == "__main__":
    main()