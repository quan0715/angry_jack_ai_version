import json

import pygame.font
import sys
import pickle

from datetime import datetime
from pygame.locals import *
from game import *
from neural_network import *
from genetic_algorithm import *
from neural_visualization import *
from setting import *


class Simulation:
    def __init__(self, mode="train", max_generation=2000):
        self.mode = mode
        self.game = GameWidget()

        self.max_generation = max_generation
        self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.log_file = open(f"log-{self.timestamp}.txt", "w")

        self.best_fitness = 0
        self.best_score = 0

        # genetic algorithm stuff
        self.individuals: List[Snake] = []

        for _ in range(GAConfig.num_population):
            # create a new individual
            snake = Snake()
            self.individuals.append(snake)

        self.current_individual = 0
        self.current_generation = 0
        self.population = Population(self.individuals)

        self._mutation_bins = np.cumsum([GAConfig.probability_gaussian,
                                         GAConfig.probability_random_uniform
                                         ])
        self._crossover_bins = np.cumsum([GAConfig.probability_SBX,
                                          GAConfig.probability_SPBX
                                          ])
        self._next_gen_size = GAConfig.num_population + GAConfig.num_offspring

        self.snake = self.population.individuals[self.current_individual]
        self.game.game_init(self.snake)

    def write_log(self, text):
        self.log_file.write(text)
        self.log_file.write("\n")
        self.log_file.flush()

    def test_snake(self, snake):
        self.mode = "test"
        self.snake = snake
        self.game.game_init(self.snake)

    def next_individual(self):
        self.snake.calculate_fitness()
        fitness = self.snake.fitness
        score = self.snake.score
        # print(self.current_individual, self.snake.score, fitness)
        if score > self.best_score:
            self.best_score = score

        if fitness > self.best_fitness:
            self.best_fitness = fitness

        self.current_individual += 1

        if (self.current_generation > 0 and self.current_individual == self._next_gen_size) or \
                (self.current_generation == 0 and self.current_individual == GAConfig.num_population):
            avg = np.mean([snake.score for snake in self.population.individuals])
            print(f'======================= Generation {self.current_generation} =======================')
            print(f'Max fitness: {self.population.fittest_individual.fitness:.2e}')
            print(f'Best Score: {self.population.fittest_individual.score}')
            print(f'Average Score: {avg:.2f}', )
            self.write_log(f"{self.current_generation} "
                           f"{self.population.fittest_individual.fitness:.2e} "
                           f"{self.population.fittest_individual.score} "
                           f"{avg:.2f}")
            self.next_generation()

        self.snake = self.population.individuals[self.current_individual]
        self.game.game_init(self.snake)

    def save_generation(self):
        networks = []
        for snake in self.population.individuals:
            networks.append(snake.network)

        metadata = {'best_score': self.best_score,
                    'best_fitness': self.best_fitness,
                    'trained_step': self.current_generation,
                    'population': networks}

        with open('best_generation.pkl', 'wb') as f:
            pickle.dump(metadata, f)

    def next_generation(self):
        self.current_generation += 1
        self.current_individual = 0

        # Calculate fitness of individuals
        for snake in self.population.individuals:
            snake.calculate_fitness()

        self.population.individuals = elitism_selection(self.population, GAConfig.num_population)
        if self.population.fittest_individual.fitness >= self.best_fitness:
            print(f"Snake saved: score {self.best_score}, fitness {self.best_fitness:.2e}")
            self.population.fittest_individual.save()
            self.save_generation()

        random.shuffle(self.population.individuals)
        next_pop: List[Snake] = [Snake(snake.network) for snake in self.population.individuals]

        while len(next_pop) < self._next_gen_size:
            p1, p2 = roulette_wheel_selection(self.population, 2)

            L = len(p1.network)
            c1_network = create_default_model()
            c2_network = create_default_model()

            # Each W_l and b_l are treated as their own chromosome.
            # Because of this I need to perform crossover/mutation on each chromosome between parents
            for l in range(L):
                p1_W_l, p1_b_l = p1.network.get_weight_and_bias(l)
                p2_W_l, p2_b_l = p2.network.get_weight_and_bias(l)

                # Crossover
                # @NOTE: I am choosing to perform the same type of crossover on the weights and the bias.
                c1_W_l, c2_W_l, c1_b_l, c2_b_l = self.crossover(p1_W_l, p2_W_l, p1_b_l, p2_b_l)

                # Mutation
                # @NOTE: I am choosing to perform the same type of mutation on the weights and the bias.
                self.mutation(c1_W_l, c2_W_l, c1_b_l, c2_b_l)

                # Assign children from crossover/mutation
                c1_network.set_weight_and_bias(l, c1_W_l, c1_b_l)
                c2_network.set_weight_and_bias(l, c2_W_l, c2_b_l)

                # Clip to [-1, 1]
                c1_network.clip_weights(l)
                c2_network.clip_weights(l)

            # Create children from chromosomes generated above
            c1 = Snake(c1_network)
            c2 = Snake(c2_network)

            # Add children to the next generation
            next_pop.extend([c1, c2])

        # Set the next generation
        random.shuffle(next_pop)
        self.population.individuals = next_pop

    def crossover(self, parent1_weights: np.ndarray, parent2_weights: np.ndarray,
                  parent1_bias: np.ndarray, parent2_bias: np.ndarray) -> Tuple[
        np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        rand_crossover = random.random()
        crossover_bucket = np.digitize(rand_crossover, self._crossover_bins)

        # Simulated binary crossover (SBX)
        if crossover_bucket == 0:
            child1_weights, child2_weights = simulated_binary_crossover(parent1_weights, parent2_weights, 100)
            child1_bias, child2_bias = simulated_binary_crossover(parent1_bias, parent2_bias, 100)

        # Single point binary crossover (SPBX)
        elif crossover_bucket == 1:
            child1_weights, child2_weights = single_point_binary_crossover(parent1_weights, parent2_weights,
                                                                           major='r')
            child1_bias, child2_bias = single_point_binary_crossover(parent1_bias, parent2_bias, major='r')

        else:
            raise Exception('Unable to determine valid crossover based off probabilities')

        return child1_weights, child2_weights, child1_bias, child2_bias

    def mutation(self, child1_weights: np.ndarray, child2_weights: np.ndarray,
                 child1_bias: np.ndarray, child2_bias: np.ndarray) -> None:
        scale = .2
        rand_mutation = random.random()
        mutation_bucket = np.digitize(rand_mutation, self._mutation_bins)
        mutation_rate = GAConfig.mutation_rate

        # Gaussian
        if mutation_bucket == 0:
            # Mutate weights
            gaussian_mutation(child1_weights, mutation_rate, scale=scale)
            gaussian_mutation(child2_weights, mutation_rate, scale=scale)

            # Mutate bias
            gaussian_mutation(child1_bias, mutation_rate, scale=scale)
            gaussian_mutation(child2_bias, mutation_rate, scale=scale)

        # Uniform random
        elif mutation_bucket == 1:
            # Mutate weights
            random_uniform_mutation(child1_weights, mutation_rate, -1, 1)
            random_uniform_mutation(child2_weights, mutation_rate, -1, 1)

            # Mutate bias
            random_uniform_mutation(child1_bias, mutation_rate, -1, 1)
            random_uniform_mutation(child2_bias, mutation_rate, -1, 1)

        else:
            raise Exception('Unable to determine valid mutation based off probabilities.')

    def run_simulation(self):
        while True:
            if self.snake.is_alive and not self.snake.win:
                self.game.update_snake()
                continue
            if self.mode == "train":
                self.next_individual()
                continue
            break


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
                counter = (counter + 1) % 10
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


def main():
    pg.init()
    pg.display.set_caption("Module Visualization")
    snake = Snake.load("best_snake.pkl")
    frame = VisualizeFrame()
    frame.run("train", snake)
    # simulation = Simulation()
    # frame = VisualizeFrame(simulation)
    # frame.run()
    # simulation = Simulation()
    # simulation.run_simulation()


if __name__ == "__main__":
    main()
