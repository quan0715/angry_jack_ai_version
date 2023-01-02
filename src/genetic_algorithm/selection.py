import random
from typing import List

from .individual import Individual
from .population import Population


def elitism_selection(population: Population, num_individuals: int) -> List[Individual]:
    individuals = sorted(population.individuals, key=lambda individual: individual.fitness, reverse=True)
    return individuals[:num_individuals]


def roulette_wheel_selection(population: Population, num_individuals: int) -> List[Individual]:
    selection = []
    wheel = sum(individual.fitness for individual in population.individuals)
    for _ in range(num_individuals):
        pick = random.uniform(0, wheel)
        current = 0
        for individual in population.individuals:
            current += individual.fitness
            if current > pick:
                selection.append(individual)
                break

    return selection
