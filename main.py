import time
import sys
import pygame as pg
import pygame.font
from pygame.locals import *
from game import Game, Direction


class GUIConfig:
    window_weight: int = 900
    window_height: int = 600
    snake_game_display_pos: tuple = 480, 20
    background_color = pg.Color("#000000")
    label_color = pg.Color("#FFFFFF")
    text_color = pg.Color("#FFFFFF")
    testing_color = pg.Color("#5C5C5C")
    label_size = 20


class VisualizeFrame:
    def __init__(self):
        self.background = pg.display.set_mode((GUIConfig.window_weight, GUIConfig.window_height))
        self.background.fill(GUIConfig.background_color)
        self.game = Game("train")
        self.game.game_init()
        self.clock = pg.time.Clock()
        self.font = pygame.font.Font('ChivoMono-Medium.ttf', GUIConfig.label_size)

    def update_game(self):
        snake_game_screen = self.game.update_window()
        self.background.blit(snake_game_screen, dest=GUIConfig.snake_game_display_pos)
    def update_label(self):
        def generate_label(label: str, value: str, start_pos):
            label = self.font.render(f'{label}: ', True, GUIConfig.label_color)
            text = self.font.render(f'{value}', True, GUIConfig.text_color)
            label_pos, text_pos = start_pos, (start_pos[0] + label.get_width(), start_pos[1])
            label_screen.blit(label, label_pos)
            label_screen.blit(text, text_pos)
            return label.get_width() + text.get_width(), label.get_height()

        label_screen = pg.Surface((400, 150))
        label_screen.fill(GUIConfig.testing_color)
        game_screen_pos = GUIConfig.snake_game_display_pos
        label_screen_pos = game_screen_pos[0], game_screen_pos[1] + 410
        generate_label("Generation", f"{0}", (5, 5))
        generate_label("Best score", f"{self.game.get_score()}", (5, GUIConfig.label_size + 5))
        generate_label("Best Fitness", f"{0}", (5, GUIConfig.label_size * 2 + 5))
        self.background.blit(label_screen, dest=label_screen_pos)
    def build(self):
        while True:
            self.clock.tick(10)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.type == K_ESCAPE:
                        sys.exit()
                    if event.key == K_RIGHT:
                        self.game.update_snake_direction(Direction.RIGHT)
                    if event.key == K_LEFT:
                        self.game.update_snake_direction(Direction.LEFT)
                    if event.key == K_UP:
                        self.game.update_snake_direction(Direction.UP)
                    if event.key == K_DOWN:
                        self.game.update_snake_direction(Direction.DOWN)

            self.update_game()
            self.update_label()
            pg.display.flip()

def main():
    pg.init()
    pg.display.set_caption("Module Visualization")
    frame = VisualizeFrame()
    frame.build()

if __name__ == "__main__":
    main()