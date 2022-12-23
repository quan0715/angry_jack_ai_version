import time
import sys
import pygame as pg
import pygame.font
from pygame.locals import *
from game import *


class GUIConfig:
    window_weight: int = 900
    window_height: int = 600
    snake_game_display_pos: tuple = 480, 20
    neural_screen_pos: tuple = 20, 20
    background_color = pg.Color("#000000")
    label_color = pg.Color("#FFFFFF")
    text_color = pg.Color("#FFFFFF")
    testing_color = pg.Color("#5C5C5C")
    label_size = 20
    first_node_pos = (20,20)
    node_space = 1
    layer_space = 120
    node_not_active_color = pg.Color('#FFFFFF')
    node_active_color = pg.Color('#79FF79')
    node_boarder_color = pg.Color('#272727')
    node_size = 8
    node_num = [32,20,12,4]
    line_not_active_color = pg.Color('#80FFFF')
    line_active_color = pg.Color('#FF0000')
    line_width = 1
    


class Layer:
    def __init__(self,screen):
        self.screen = screen
    def draw(self):
        node=Node(self.screen)
        node.draw()

class Node:
    def __init__(self,screen):
        self.screen = screen

    def draw(self):
        for l in range(len(GUIConfig.node_num)):
            upper_space = (GUIConfig.window_height-GUIConfig.first_node_pos[1]-GUIConfig.node_num[l]*(GUIConfig.node_size*2+GUIConfig.node_space))/2
            for i in range(GUIConfig.node_num[l]):
                pg.draw.circle(self.screen,GUIConfig.node_boarder_color,(GUIConfig.first_node_pos[0]+l*GUIConfig.layer_space,upper_space+i*(2*GUIConfig.node_size+GUIConfig.node_space)),GUIConfig.node_size)
                pg.draw.circle(self.screen,GUIConfig.node_not_active_color,(GUIConfig.first_node_pos[0]+l*GUIConfig.layer_space,upper_space+i*(2*GUIConfig.node_size+GUIConfig.node_space)),GUIConfig.node_size-1)

        for l in range(len(GUIConfig.node_num)-1):
            upper_space_pre = (GUIConfig.window_height-GUIConfig.first_node_pos[1]-GUIConfig.node_num[l]*(GUIConfig.node_size*2+GUIConfig.node_space))/2
            upper_space_nxt = (GUIConfig.window_height-GUIConfig.first_node_pos[1]-GUIConfig.node_num[l+1]*(GUIConfig.node_size*2+GUIConfig.node_space))/2
            for i in range(GUIConfig.node_num[l]):
                for j in range(GUIConfig.node_num[l+1]):
                    pg.draw.line(self.screen,GUIConfig.line_not_active_color,(GUIConfig.first_node_pos[0]+l*GUIConfig.layer_space+GUIConfig.node_size,upper_space_pre+i*(2*GUIConfig.node_size+GUIConfig.node_space)),(GUIConfig.first_node_pos[0]+(l+1)*GUIConfig.layer_space-GUIConfig.node_size,upper_space_nxt+j*(2*GUIConfig.node_size+GUIConfig.node_space)),GUIConfig.line_width)
        
        decision_font = pygame.font.Font('ChivoMono-Medium.ttf', 16)
        decision_label = [decision_font.render("U", True, (0,0,0)), decision_font.render("D", True, (0,0,0)), decision_font.render("L", True, (0,0,0)), decision_font.render("R", True, (0,0,0))]
        for i in range(len(decision_label)):
            self.screen.blit(decision_label[i], (GUIConfig.first_node_pos[0]+(len(GUIConfig.node_num)-1)*GUIConfig.layer_space+GUIConfig.node_size+5, upper_space+i*(2*GUIConfig.node_size+GUIConfig.node_space)-10))

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
            # return label.get_width() + text.get_width(), label.get_height()

        label_screen = pg.Surface((400, 150))
        label_screen.fill(GUIConfig.testing_color)
        game_screen_pos = GUIConfig.snake_game_display_pos
        label_screen_pos = game_screen_pos[0], game_screen_pos[1] + Config.map_max_height + 10
        generate_label("Generation", f"{0}", (5, 5))
        generate_label("Best score", f"{self.game.get_score()}", (5, GUIConfig.label_size + 5))
        generate_label("Best Fitness", f"{0}", (5, GUIConfig.label_size * 2 + 5))
        self.background.blit(label_screen, dest=label_screen_pos)

    def update_neural(self):
        neural_screen = pg.Surface((450, 560))
        neural_screen.fill(GUIConfig.testing_color)
        self.layer = Layer(neural_screen)
        self.layer.draw()
        self.background.blit(neural_screen, dest=GUIConfig.neural_screen_pos)
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
            self.update_neural()
            pg.display.flip()

def main():
    pg.init()
    pg.display.set_caption("Module Visualization")
    frame = VisualizeFrame()
    frame.build()

if __name__ == "__main__":
    main()