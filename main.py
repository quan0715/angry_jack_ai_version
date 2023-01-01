import pygame.font
import sys

from pygame.locals import *
from game import *
from neural_network import *
from genetic_algorithm import *
from neural_visualization import *
from setting import *


class Simulation:
    def __init__(self, mode="train"):
        self.mode = mode
        self.game = Game()

        # genetic algorithm stuff
        self.individuals: List[Snake] = []

        for _ in range(GAConfig.num_population):
            # create a new individual
            snake = Snake()
            self.individuals.append(snake)

        self.best_fitness = 0
        self.best_score = 0

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

    def next_individual(self):
        self.snake.calculate_fitness()
        fitness = self.snake.fitness
        # print(self.current_individual, self.snake.score, fitness)

        if fitness > self.best_fitness:
            self.best_fitness = fitness
            # TODO update label

        self.current_individual += 1

        if (self.current_generation > 0 and self.current_individual == self._next_gen_size) or \
                (self.current_generation == 0 and self.current_individual == GAConfig.num_population):
            print(
                '======================= Gneration {} ======================='.format(self.current_generation))
            print('----Max fitness:', self.population.fittest_individual.fitness)
            print('----Best Score:', self.population.fittest_individual.score)
            print('----Average fitness:', self.population.average_fitness)
            self.next_generation()

        self.snake = self.population.individuals[self.current_individual]
        self.game.game_init(self.snake)

    def increment_generation(self):
        self.current_generation += 1
        # TODO update label

    def next_generation(self):
        self.increment_generation()
        self.current_individual = 0

        # Calculate fitness of individuals
        for snake in self.population.individuals:
            snake.calculate_fitness()

        self.population.individuals = elitism_selection(self.population, GAConfig.num_population)
        if self.population.fittest_individual.fitness >= self.best_fitness:
            self.population.fittest_individual.save()

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
            if self.snake.is_alive:
                self.game.update_snake()
            else:
                self.next_individual()


class VisualizeFrame:
    def __init__(self):
        self.background = pg.display.set_mode(GUIConfig.main_window_size)
        self.background.fill(GUIConfig.background_color)
        self.clock = pg.time.Clock()
        self.font = pygame.font.Font(GUIConfig.font_family, GUIConfig.label_size)
        self.neural_vis = NeuralVisualize()
        self.simulation = Simulation()

    def update_game(self):
        self.simulation.game.update_snake()
        snake_game_screen = self.simulation.game.update_window()
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
        generate_label("Best score", f"{self.simulation.snake.score}", (5, GUIConfig.label_size + 5))
        generate_label("Best Fitness", f"{0}", (5, GUIConfig.label_size * 2 + 5))
        generate_label("Network layers", f"{GAConfig.hidden_layer_size}", (5, GUIConfig.label_size * 3 + 5))
        self.background.blit(label_screen, dest=label_screen_pos)

    def update_neural(self):
        neural_screen = pg.Surface((GUIConfig.network_window_size[0], GUIConfig.network_window_size[1]))
        # neural_screen.fill(GUIConfig.testing_color)
        snake:Snake=self.simulation.game.snake
        network_outputs:list[np.ndarray] = snake.network.last_outputs
        snake_feature = [bool(f) for f in snake.get_feature()]
        output_feature = snake_feature[24:28]
        # TODO update neural visualization
        self.neural_vis.update_network([snake_feature, network_outputs[0], network_outputs[1], output_feature])
        self.neural_vis.draw(neural_screen)
        self.background.blit(neural_screen, dest=GUIConfig.neural_screen_pos)

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

            if self.simulation.mode == "manual" or self.simulation.mode == "slow":
                counter = (counter + 1) % 10
                if counter: continue

            if self.simulation.snake.is_alive:
                self.update_game()
                self.update_label()
                self.update_neural()
            else:
                self.simulation.next_individual()

            pg.display.flip()


def main():
    # pg.init()
    # pg.display.set_caption("Module Visualization")
    # frame = VisualizeFrame()
    # frame.run()
    simulation = Simulation()
    simulation.run_simulation()


if __name__ == "__main__":
    main()
