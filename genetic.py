import random

# creates a list of 64 ints in range (0 - 255)
def create_population(population_size):
    return [[random.randint(0, 255) for i in range(64)] for j in range(population_size)]

def evaluate_population(population, vm):
    fitness_scores = []

    for program in population:
        treasures = vm.run(program)
        moves = vm.environment.moves_count

        if treasures == 0:
            fitness = 0
        else:
            #fitness = treasures
            fitness = treasures + 1 / (moves + 1)

        fitness_scores.append(fitness)

    return fitness_scores

def tournament_selection(population, fitness_scores, tournament_size=3):
    candidates = random.sample(
        range(len(population)),
        tournament_size
    )

    winner_index = max(
        candidates,
        key=lambda index: fitness_scores[index]
    )

    return population[winner_index].copy()

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)

    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    return child1, child2

def mutate(program, mutation_rate=0.02):
    mutated = program.copy()

    for index in range(len(mutated)):
        if random.random() < mutation_rate:
            mutated[index] = random.randint(0, 255)

    return mutated


def next_generation(population, fitness_scores, mutation_rate=0.02, selection_method="tournament"):
    best_index = max(
        range(len(population)),
        key=lambda index: fitness_scores[index]
    )

    # Elitism save the best individual frpm the previous population
    new_population = [population[best_index].copy()]

    if selection_method == "tournament":
        select_parent = tournament_selection
    elif selection_method == "roulette":
        select_parent = roulette_selection
    else:
        raise ValueError("Unknown selection method.")

    while len(new_population) < len(population):
        parent1 = select_parent(population, fitness_scores)
        parent2 = select_parent(population, fitness_scores)

        child1, child2 = crossover(parent1, parent2)

        new_population.append(mutate(child1, mutation_rate))

        if len(new_population) < len(population):
            new_population.append(mutate(child2, mutation_rate))

    return new_population

def roulette_selection(population, fitness_scores):
    if sum(fitness_scores) == 0:
        return random.choice(population).copy()

    winner = random.choices(population,weights=fitness_scores,k=1)[0]

    return winner.copy()