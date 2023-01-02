import sys

import pygame.font
from pygame.locals import *

from game import *
from neural_visualization import *
from config.setting import *
from simulation import Simulation


class LabelsDisplayWidget(PygameLayout):
    def __init__(self):
        start_pos = Point(GUIConfig.snake_game_display_pos[0],
                          GUIConfig.snake_game_display_pos[1] + GameConfig.map_max_height + 10)
        height, width = GUIConfig.label_screen_size
        super().__init__(start_pos, height, width)
        self.font = pygame.font.Font(GUIConfig.font_family, GUIConfig.label_size)
        self.label_start_pos = Point(5, 5)
        self.label_dict = None

    def draw(self, win):
        screen = self.get_screen()
        for idx, item in enumerate(self.label_dict.items()):
            label = self.font.render(f'{item[0]}: ', True, GUIConfig.label_color)
            text = self.font.render(f'{item[1]}', True, GUIConfig.text_color)
            row_x, row_y = self.label_start_pos.x, self.label_start_pos.y + GUIConfig.label_size * idx
            screen.blit(label, (row_x, row_y))
            screen.blit(text, (row_x + label.get_width(), row_y))

        win.blit(screen, self.get_start_pos().get_point())

    def set_label(self, label_dict: dict):
        self.label_dict = label_dict


class VisualizeFrame(PygameLayout):
    def __init__(self, simulation=None):
        super().__init__(Point(0, 0), GUIConfig.main_window_size[0], GUIConfig.main_window_size[1])
        self.background = pg.display.set_mode(self.get_size())
        self.background.fill(GUIConfig.background_color)
        self.clock = pg.time.Clock()
        self.neural_vis = NeuralVisualizeWidget()
        self.label_vis = LabelsDisplayWidget()
        self.simulation = simulation
        if simulation is None:
            self.simulation = Simulation()

    def update_game(self):
        self.simulation.game.update_snake()
        self.simulation.game.draw(self.background)

    def update_label(self):
        if self.simulation.mode == 'test':
            self.label_vis.set_label({
                'Score': self.simulation.snake.score}
            )
        else:
            self.label_vis.set_label({
                "Generation": f"{self.simulation.current_generation}",
                "Individual": f"{self.simulation.current_individual}/{GAConfig.num_population}",
                "Best score": f"{self.simulation.best_score}",
                "Best fitness": f"{self.simulation.best_fitness}",
                "Mutation rate": f"{GAConfig.mutation_rate}",
                "Number of population": f"{GAConfig.num_population}",
            })

        self.label_vis.draw(self.background)

    def update_neural(self):
        snake: Snake = self.simulation.game.snake
        network_outputs: List[np.ndarray] = snake.network.last_outputs
        snake_feature = [bool(f) for f in snake.get_feature()]
        self.neural_vis.update_network([snake_feature, network_outputs[0], network_outputs[1], network_outputs[2]])
        self.neural_vis.draw(self.background)

    def read_keyboard(self, event):
        if event.type == KEYDOWN and self.simulation.mode == "manual":
            if event.type == K_ESCAPE:
                sys.exit()
            if event.key == K_RIGHT:
                self.snake.look_in_direction(Direction.RIGHT)
            if event.key == K_LEFT:
                self.snake.look_in_direction(Direction.LEFT)
            if event.key == K_UP:
                self.snake.look_in_direction(Direction.UP)
            if event.key == K_DOWN:
                self.snake.look_in_direction(Direction.DOWN)

    def run(self):
        counter = 0
        while True:
            self.clock.tick(GameConfig.game_fps)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                self.read_keyboard(event)

            if self.simulation.mode == "manual" or self.simulation.mode == "test":
                counter = (counter + 1) % GameConfig.update_rate
                if counter: continue

            if self.simulation.snake.is_alive and not self.simulation.snake.win:
                self.update_game()
                self.update_label()
                self.update_neural()
            else:
                if self.simulation.mode == "test":
                    self.simulation.snake.respawn()
                else:
                    self.simulation.next_individual()

            pg.display.flip()
