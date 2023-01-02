import pickle
from datetime import datetime

from game import *
from genetic_algorithm import *
from neural_network import *
from neural_visualization import *
from config.setting import *


class Simulation:
    def __init__(self, mode="train", max_generation=2000, save_log=False, init_snake:Optional[Snake] = None):
        self.mode = mode
        self.game = GameWidget()

        self.max_generation = max_generation
        if save_log:
            self.timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            self.log_file = open(f"logs/log-{self.timestamp}.txt", "w")

        self.best_fitness = 0
        self.best_score = 0

        self.current_individual = 0
        self.current_generation = 0
        
        if init_snake is not None:
            self.individuals = [init_snake] * GAConfig.num_population
        else:
            # genetic algorithm stuff
            self.individuals: List[Snake] = []

            for _ in range(GAConfig.num_population):
                # create a new individual
                snake = Snake()
                self.individuals.append(snake)

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
        if not self.log_file: return
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

        with open('resources/best_generation.pkl', 'wb') as f:
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

            # snake is dead
            if self.current_generation >= self.max_generation:
                print("Reached max generation.")
                return

            if self.mode == "train":
                self.next_individual()
                continue
            if self.mode == "test":
                print("Test Score:", self.snake.score)
                break
