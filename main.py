from pathlib import Path
import random
import matplotlib.pyplot as plt
from compare import plot_results, plot_fitness
from environment import Environment
from virtmachine import VirtualMachine
from genetic import create_population, evaluate_population, next_generation


folder = Path(__file__).resolve().parent


def ask_to_continue():
    while True:
        answer = input(
            "\nGeneration limit reached. Continue? (y/n): "
        ).strip().lower()

        if answer == "y":
            return True
        if answer == "n":
            return False



# Load the map.
with open(folder / "map.txt", encoding="utf-8") as file:
    rows, columns = map(int, file.readline().split())
    start = tuple(map(int, file.readline().split()))
    treasure_count = int(file.readline())

    treasures = [
        tuple(map(int, file.readline().split()))
        for _ in range(treasure_count)
    ]

environment = Environment(rows, columns, start, treasures)
vm = VirtualMachine(environment)

seed_limit = 10

population_size = 100
population = create_population(population_size)
generation_limit = 20
selection_method = "tournament"

generation = 0

all_histories = []
history = []
generations_to_success = []

for seed in range(1, seed_limit+1):
    random.seed(seed)

    generation = 0
    stagnation_count = 0
    best_so_far = 0
    history = []
    population = create_population(20)

    print(f"\nSeed: {seed}")

    while True:
        generation += 1
    
        fitness_scores = evaluate_population(population, vm)

        best_index = max(range(len(population)), key=lambda index: fitness_scores[index])

        best_program = population[best_index].copy()
        best_fitness = fitness_scores[best_index]
        history.append((generation, best_fitness, sum(fitness_scores) / len(fitness_scores)))
        average_fitness = sum(fitness_scores) / len(fitness_scores)

        print(
            f"Generation {generation}: "
            f"best={best_fitness}, average={average_fitness:.2f}")
    
        # Stop if a program collects every treasure. !!!!! I need to uncomment this before submission
        treasures_found = vm.run(best_program)
        if treasures_found == len(environment.initial_treasures):
            generations_to_success.append(generation)
            break

        

        if generation % generation_limit == 0:
            vm.run(best_program)
            print("Best program:", best_program)
            print("Output:", vm.output)
            environment.display()

            # UNcommNET BEFORE SUBMISSION 
            if not ask_to_continue():
                generations_to_success.append(None)  
                break

        if best_fitness > best_so_far:
            best_so_far = best_fitness
            stagnation_count = 0
        else:
            stagnation_count += 1    

        if stagnation_count >= 200:
            for i in range(len(population) // 2, len(population)):
                population[i] = [random.randint(0, 255) for _ in range(64)]

            stagnation_count = 0    
        else:    
            population = next_generation(population, fitness_scores, selection_method=selection_method)

    all_histories.append(history.copy())    


    with open(
        folder / f"history_{selection_method}_{seed}.csv",
        "w",
        encoding="utf-8"
    ) as file:
        file.write("generation,best_fitness,average_fitness\n")

        for number, best, average in history:
            file.write(f"{number},{best},{average}\n")


print(f"{selection_method}: {generations_to_success}")  
plot_results(generations_to_success, selection_method, folder)
plot_fitness(all_histories, selection_method, folder)          



# Display the best program from the final evaluated generation.
vm.run(best_program)

print("\nBest program:", best_program)
environment.display()
print("Output:", vm.output)
print("Instructions executed:", vm.instructions_executed)