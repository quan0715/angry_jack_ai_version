from typing import List
import numpy as np
from setting import *
from misc import *
import pygame as pg


class NeuralVisualizeWidget(PygameLayout):
    def __init__(self):
        size_config = GUIConfig.network_window_size
        super().__init__(Point(*GUIConfig.neural_screen_pos), size_config[0], size_config[1])
        self.layers_node_num = [32, *GAConfig.hidden_layer_size, 4]
        self.start_point = Point(GUIConfig.node_size, GUIConfig.node_size)
        self.layer_space = (self.get_width() - self.start_point.x * 2) / len(self.layers_node_num)
        self.layers: List[LayerWidget] = []
        self.build_network()

    def build_network(self):
        start_x = self.start_point.x
        for layer_idx, node_num in enumerate(self.layers_node_num):
            self.layers.append(LayerWidget(node_num, start_x + self.layer_space * layer_idx))

    def update_network(self, features: List[np.array]):
        for layer, feature in zip(self.layers, features):
            layer.update_layer(feature)

    def _draw_output_layer_label(self, screen):
        decision_font = pg.font.Font(GUIConfig.font_family, 16)
        decision_label = [decision_font.render(direction, True, GUIConfig.label_color) for direction in
                          ('U', 'D', 'L', 'R')]
        for label, node in zip(decision_label, self.layers[-1].nodes):
            node_pos_x, node_pos_y = node.center_pos.get_point()
            screen.blit(label, (node_pos_x + 10, node_pos_y - 10))

    def draw(self, win):
        screen = self.get_screen()
        # screen.fill(GUIConfig.testing_color)
        for idx in range(len(self.layers_node_num)):
            if idx != len(self.layers_node_num) - 1:
                self.layers[idx].connect_with_layer(self.layers[idx + 1], screen)
            self.layers[idx].draw(screen)
        self._draw_output_layer_label(screen)
        win.blit(screen, self.get_start_pos().get_point())


class LayerWidget:
    def __init__(self, node_number: int, start_x: Union[int, float]):
        self.start_x = start_x
        self.node_number = node_number
        space_of_each_node = 2 * GUIConfig.node_size + GUIConfig.node_space
        self.start_y = (GUIConfig.node_size * 2 + GUIConfig.network_window_size[1] - self.node_number * space_of_each_node - GUIConfig.node_space) / 2
        self.nodes = [NodeWidget(Point(self.start_x, self.start_y + idx * space_of_each_node)) for idx in
                      range(node_number)]

    def connect_with_layer(self, target_layer, screen):
        for node in self.nodes:
            for target_layer_node in target_layer.nodes:
                node.connect_with_line(target_layer_node, screen=screen)

    def update_layer(self, feature: List[bool] = None):
        if feature is None or len(feature) != self.node_number:
            feature = [False for _ in range(self.node_number)]
        for node, f in zip(self.nodes, feature):
            node.update_status(f)

    def draw(self, win: pg.Surface):
        for node in self.nodes:
            node.draw(win)


class NodeWidget:
    def __init__(self, center_pos: Point, status=False):
        self.center_pos: Point = center_pos  # center
        self.status: bool = False
        self.node_color: pg.Color = GUIConfig.node_active_color
        self.line_color: pg.Color = GUIConfig.line_active_color

    def update_status(self, status: bool):
        self.status = status
        self.node_color = GUIConfig.node_active_color if self.status else GUIConfig.node_not_active_color
        self.line_color = GUIConfig.line_active_color if self.status else GUIConfig.line_not_active_color

    def connect_with_line(self, target_node: 'NodeWidget', screen):
        pg.draw.line(screen, self.line_color, self.center_pos.get_point(), target_node.center_pos.get_point(),
                     GUIConfig.line_width)

    def draw(self, screen: pg.Surface):
        pg.draw.circle(screen, GUIConfig.node_boarder_color, self.center_pos.get_point(), GUIConfig.node_size)  # border
        pg.draw.circle(screen, self.node_color, self.center_pos.get_point(), GUIConfig.node_size - 1)  # inside
