import time
import sys
from typing import List

import pygame as pg
import pygame.font
from pygame.locals import *
from game import *
from setting import *

class NeuralVisualize:
    def __init__(self,screen):
        self.screen = screen
        
    def draw(self):
        node_space = GUIConfig.node_space
        layer_space = GUIConfig.layer_space
        radius = GUIConfig.node_size
        first_posX = GUIConfig.first_node_pos[0]
        first_posY = GUIConfig.first_node_pos[1]
        layer_nodes = GUIConfig.layer_nodes
        
        # draw node
        for layer, node_num in enumerate(GUIConfig.layer_nodes):
            lw = LayerWidget(layer)
            lw.draw(self.screen)
        # draw line
        for l in range(1, len(layer_nodes)):
            pre_layer_num_nodes = layer_nodes[l-1]
            cur_layer_num_nodes = layer_nodes[l]
            upper_space_pre = (GUIConfig.window_height-first_posY-pre_layer_num_nodes*(radius*2+node_space))/2
            upper_space_nxt = (GUIConfig.window_height-first_posY-cur_layer_num_nodes*(radius*2+node_space))/2
            for i in range(pre_layer_num_nodes):
                line_start = (first_posX+(l-1)*layer_space+radius,upper_space_pre+i*(2*radius+node_space))
                for j in range(cur_layer_num_nodes):
                    line_end = (first_posX+l*layer_space-radius,upper_space_nxt+j*(2*radius+node_space))
                    pg.draw.line(self.screen,GUIConfig.line_not_active_color, line_start, line_end, GUIConfig.line_width)

        # draw label
        upper_space = (GUIConfig.window_height-first_posY-layer_nodes[len(layer_nodes)-1]*(radius*2+node_space))/2
        decision_font = pygame.font.Font('ChivoMono-Medium.ttf', 16)
        decision_label = [decision_font.render("U", True, (0,0,0)),
                            decision_font.render("D", True, (0,0,0)),
                            decision_font.render("L", True, (0,0,0)),
                            decision_font.render("R", True, (0,0,0))]
        for i in range(len(decision_label)):
            self.screen.blit(decision_label[i], (first_posX+(len(layer_nodes)-1)*layer_space+radius+5, upper_space+i*(2*radius+node_space)-10))

class NodeWidget:
    def __init__(self, center_pos: Point, status= False):
        self.center_pos = center_pos # center
        self.status = status
        self.color = GUIConfig.node_active_color if self.status else GUIConfig.node_not_active_color
    def update_status(self, status: bool):
        self.status = status
        self.color = GUIConfig.node_active_color if self.status else GUIConfig.node_not_active_color
    def draw(self, screen: pg.Surface):
        border_color = GUIConfig.node_boarder_color
        node_size = GUIConfig.node_size
        pg.draw.circle(screen, border_color, self.center_pos.get_point(), node_size) # border
        pg.draw.circle(screen, self.color, self.center_pos.get_point(), node_size - 1) # inside

class LayerWidget:
    def __init__(self, layer: int):
        first_posX = GUIConfig.first_node_pos[0]
        first_posY = GUIConfig.first_node_pos[1]
        layer_nodes = GUIConfig.layer_nodes
        radius = GUIConfig.node_size
        node_space = GUIConfig.node_space
        layer_space = GUIConfig.layer_space
        upper_space = (GUIConfig.window_height-first_posY-layer_nodes[layer]*(radius*2+node_space))/2
        self.nodes = [NodeWidget(Point(first_posX+layer*layer_space, upper_space+i*(2*radius+node_space))) for i in range(layer_nodes[layer])]
    def draw(self, screen: pg.Surface):
        for node in self.nodes:
            node.draw(screen)


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
        label_screen_pos = game_screen_pos[0], game_screen_pos[1] + GameConfig.map_max_height + 10
        generate_label("Generation", f"{0}", (5, 5))
        generate_label("Best score", f"{self.game.get_score()}", (5, GUIConfig.label_size + 5))
        generate_label("Best Fitness", f"{0}", (5, GUIConfig.label_size * 2 + 5))
        self.background.blit(label_screen, dest=label_screen_pos)
    def update_neural(self):
        neural_screen = pg.Surface((450, 560))
        neural_screen.fill(GUIConfig.testing_color)
        self.neural_vis = NeuralVisualize(neural_screen)
        self.neural_vis.draw()
        self.background.blit(neural_screen, dest=GUIConfig.neural_screen_pos)
    def build(self):
        counter=0
        while True:
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

def main():
    pg.init()
    pg.display.set_caption("Module Visualization")
    frame = VisualizeFrame()
    frame.build()

if __name__ == "__main__":
    main()