import time
import sys
from typing import List

import pygame as pg
import pygame.font
from pygame.locals import *
from neural_visualization import *
from game import *
from setting import *
class VisualizeFrame:
    def __init__(self):
        self.background = pg.display.set_mode(GUIConfig.main_window_size)
        self.background.fill(GUIConfig.background_color)
        self.game = Game("train")
        self.game.game_init()
        self.clock = pg.time.Clock()
        self.font = pygame.font.Font(GUIConfig.font_family, GUIConfig.label_size)
        self.neural_vis: NeuralVisualize = NeuralVisualize()
    def update_game(self):
        snake_game_screen = self.game.update_window()
        self.game.game_over = self.game.snake.check_wall_collision() or self.game.snake.check_body_collision()
        self.background.blit(snake_game_screen, dest=GUIConfig.snake_game_display_pos)
    def update_label(self):
        def generate_label(label: str, value: str, start_pos):
            label = self.font.render(f'{label}: ', True, GUIConfig.label_color)
            text = self.font.render(f'{value}', True, GUIConfig.text_color)
            label_pos, text_pos = start_pos, (start_pos[0] + label.get_width(), start_pos[1])
            label_screen.blit(label, label_pos)
            label_screen.blit(text, text_pos)
        label_screen = pg.Surface(GUIConfig.label_screen_size)
        # label_screen.fill(GUIConfig.testing_color)
        game_screen_pos = GUIConfig.snake_game_display_pos
        label_screen_pos = game_screen_pos[0], game_screen_pos[1] + GameConfig.map_max_height + 10
        generate_label("Generation", f"{0}", (5, 5))
        generate_label("Best score", f"{self.game.get_score()}", (5, GUIConfig.label_size + 5))
        generate_label("Best Fitness", f"{0}", (5, GUIConfig.label_size * 2 + 5))
        generate_label("Network layers", f"{NetworkConfig.layers_node_num}", (5, GUIConfig.label_size * 3 + 5))
        self.background.blit(label_screen, dest=label_screen_pos)
    def update_neural(self):
        neural_screen = pg.Surface((GUIConfig.network_window_size[0], GUIConfig.network_window_size[1]))
        # neural_screen.fill(GUIConfig.testing_color)
        snake_feature = [bool(f) for f in self.game.snake.get_feature(self.game.fruit)]
        output_feature = snake_feature[24:28]
        self.neural_vis.update_network([snake_feature,[],[],output_feature])
        self.neural_vis.draw(neural_screen)
        self.background.blit(neural_screen, dest=GUIConfig.neural_screen_pos)
    def build(self):
        counter=0
        while not self.game.game_over:
            self.clock.tick(100)
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
            counter=(counter+1)%10
            if counter: continue
            self.update_game()
            self.update_label()
            self.update_neural()
            pg.display.flip()

        self.game.game_init()
def main():
    pg.init()
    pg.display.set_caption("Module Visualization")
    frame = VisualizeFrame()
    while True:
        frame.build()

if __name__ == "__main__":
    main()