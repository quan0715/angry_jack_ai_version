from typing import List
import numpy as np
from setting import *
from misc import  *
import pygame as pg
class NeuralVisualize:
    def __init__(
            self,
            input_layer_node_num: int = NetworkConfig.input_layer_num,
            hidden_layers_num: List[int]  = NetworkConfig.hidden_layers_num,
            output_layer_node_num: int = NetworkConfig.output_layer_num):
        self.node_space, self.layer_space = GUIConfig.node_space, GUIConfig.layer_space
        self.radius = GUIConfig.node_size
        self.first_pos: Point = Point(*GUIConfig.first_node_pos)
        self.input_layer_node_num = input_layer_node_num
        self.hidden_layers_num = hidden_layers_num
        self.output_layer_node_num = output_layer_node_num
        self.total_layer_num: int = 2 + len(self.hidden_layers_num)
        self.input_layer: LayerWidget| None = None
        self.hidden_layers: List[LayerWidget]| None = None
        self.output_layer: LayerWidget| None = None
        self.build_network()

    def build_network(self):
        start_x, start_y = self.first_pos.get_point()
        self.input_layer = LayerWidget(self.input_layer_node_num, start_x)
        self.hidden_layers = [
            LayerWidget(node_num, start_x + GUIConfig.layer_space * layer_idx) for layer_idx, node_num in enumerate(self.hidden_layers_num, start=1)
        ]
        output_start_x = start_x + GUIConfig.layer_space * (self.total_layer_num - 1)
        self.output_layer = LayerWidget(self.output_layer_node_num, output_start_x)


    def draw(self, screen, features: List[np.array]):
        input_feature = features[0]
        self.input_layer.connect_with_layer(self.hidden_layers[0], screen)
        for idx in range(1, len(self.hidden_layers)):
            self.hidden_layers[idx - 1].connect_with_layer(self.hidden_layers[idx], screen)
        self.hidden_layers[-1].connect_with_layer(self.output_layer, screen)
        self.input_layer.draw(screen, feature=input_feature)
        for h_l in self.hidden_layers:
            h_l.draw(screen)
        self.output_layer.draw(screen)
        # draw output layer label
        decision_font = pg.font.Font('ChivoMono-Medium.ttf', 16)
        decision_label = [decision_font.render(l, True, (0, 0, 0)) for l in ('U', 'D', 'L', 'R')]
        for label, node in zip(decision_label, self.output_layer.nodes):
            node_pos_x, node_pos_y = node.center_pos.get_point()
            screen.blit(label,(node_pos_x + 10, node_pos_y))


class NodeWidget:
    def __init__(self, center_pos: Point, status=False):
        self.center_pos = center_pos  # center
        self.status = status
        self.node_color = GUIConfig.node_active_color if self.status else GUIConfig.node_not_active_color
        self.line_color = GUIConfig.line_active_color if self.status else GUIConfig.line_not_active_color

    def update_status(self, status: bool):
        self.status = status
        self.node_color = GUIConfig.node_active_color if self.status else GUIConfig.node_not_active_color
        self.line_color = GUIConfig.line_active_color if self.status else GUIConfig.line_not_active_color
    def connect_with_line(self, target_node: 'NodeWidget', screen):
        # line_color = GUIConfig.line_active_color if self.status else GUIConfig.line_not_active_color
        pg.draw.line(screen, self.line_color, self.center_pos.get_point(), target_node.center_pos.get_point(), GUIConfig.line_width)

    def draw(self, screen: pg.Surface, status: bool = True):
        self.update_status(status)
        border_color = GUIConfig.node_boarder_color
        node_size = GUIConfig.node_size
        pg.draw.circle(screen, border_color, self.center_pos.get_point(), node_size)  # border
        pg.draw.circle(screen, self.node_color, self.center_pos.get_point(), node_size - 1)  # inside


class LayerWidget:
    def __init__(self, node_number: int, start_x: int):
        self.start_x = start_x
        self.node_number = node_number
        space_of_each_node = 2 * GUIConfig.node_size + GUIConfig.node_space
        self.start_y = (20 + GUIConfig.network_window_height - self.node_number * space_of_each_node - GUIConfig.node_space) / 2
        self.nodes = [NodeWidget(Point(self.start_x, self.start_y + idx * space_of_each_node)) for idx in range(node_number)]

    def connect_with_layer(self, target_layer, screen):
        for node in self.nodes:
            for target_layer_node in target_layer.nodes:
                node.connect_with_line(target_layer_node, screen=screen)

    def draw(self, screen: pg.Surface, feature: List = None):
        feature = [False for _ in self.nodes] if feature is None else feature  # for debugging and testing
        for node, f in zip(self.nodes, feature):
            node.draw(screen, f)
