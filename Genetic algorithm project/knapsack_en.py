import random
import matplotlib.pyplot as plt

# CONFIGURATION AND DATA
POPULATION_SIZE = 50 # Number of backpacks in one generation
GENES_COUNT = 20 # Number of available items
GENERATIONS = 1000 # Number of generations
MUTATION_RATE = 0.05 # Mutation chance (5%)

MAX_WEIGHT = 50 # Backpack weight limit
MAX_WEAR = 30 # Backpack wear limit (third parameter)

# PATIENCE CONFIGURATION
PATIENCE = 100
best_overall_fitness = 0
stagnation_counter = 0

# Generating random items
items = [
    {"value": random.randint(10, 50),
     "weight": random.randint(1, 15),
     "wear": random.randint(1, 10)}
     for _ in range(GENES_COUNT)
]

# FITNESS FUNCTION
def calculate_fitness(chromosome):
    total_value = 0
    total_weight = 0
    total_wear = 0

    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            total_value += items[i]["value"]
            total_weight += items[i]["weight"]
            total_wear += items[i]["wear"]

    # Case where weight or wear limit is exceeded
    if total_weight > MAX_WEIGHT or total_wear > MAX_WEAR:
        return 0
    
    return total_value

# GENETIC OPERATIONS
def create_population():
    return [[random.randint(0, 1) for _ in range(GENES_COUNT)] for _ in range(POPULATION_SIZE)] 
    
def crossover(parent1, parent2):
    # Single-point crossover: take a portion of genes from each parent
    point = random.randint(1, GENES_COUNT - 1)
    child = parent1[:point] + parent2[point:]
    return child 

def mutate(chromosome):
    for i in range(len(chromosome)):
        if random.random() < MUTATION_RATE:
            chromosome[i] = 1 - chromosome[i]
    return chromosome

# MAIN ALGORITHM LOOP
best_local_backpacks = []
population = create_population()

print(f"{'Gen':<5} | {'Best Value':<10} | {'Status'}")
print("-"*35)

population_counter = 0

for gen in range(GENERATIONS):
    population = sorted(population, key=lambda x: calculate_fitness(x), reverse=True)
    best_fitness = calculate_fitness(population[0])
    best_local_backpacks.append(calculate_fitness(population[0]))
    population_counter += 1

    if best_fitness > best_overall_fitness:
        best_overall_fitness = best_fitness
        stagnation_counter = 0
    else:
        stagnation_counter += 1

    if stagnation_counter >= PATIENCE:
        print(f"--- STOP: Stagnation at generation {gen}. No improvement for {PATIENCE} generations. ---")
        break

    if gen % 10 == 0:
        print(f"{gen:<5} | {best_fitness:<10} | Optimizing...")

    # Elitism: keep the two best individuals for the next generation
    new_population = population[:2] 

    while len(new_population) < POPULATION_SIZE:
        p1, p2 = random.sample(population[:POPULATION_SIZE // 2], 2)
        child = crossover(p1, p2)
        child = mutate(child)
        new_population.append(child)
        population = new_population

# DISPLAY FINAL RESULTS
best_backpack = population[0]
final_value = calculate_fitness(best_backpack)
final_weight = sum(items[i]["weight"] for i in range(GENES_COUNT) if best_backpack[i] == 1)
final_wear = sum(items[i]["wear"] for i in range(GENES_COUNT) if best_backpack[i] == 1)

print("-"*35)
print(f"BEST BACKPACK AFTER {GENERATIONS} GENERATIONS:")
print(f"Value: {final_value}")
print(f"Weight: {final_weight}/{MAX_WEIGHT}")
print(f"Wear: {final_wear}/{MAX_WEAR}")

# PLOTS
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10))

# Plot 1: Fitness History
ax1.plot(range(1, population_counter+1), best_local_backpacks)
ax1.set_title("Evolution Progress (Backpack Value)", fontsize=16, fontweight="bold")
ax1.set_xlabel("Generation", fontsize=12)
ax1.set_ylabel("Best Fitness (Value)", fontsize=12)
ax1.grid(True)

# Plot 2: Resource Usage
labels = ["Weight", "Wear"]
current_values = [final_weight, final_wear]
max_values = [MAX_WEIGHT, MAX_WEAR]

ax2.bar(labels, max_values, color="lightgrey", label="Limit")
bars = ax2.bar(labels, current_values, color=["skyblue", "salmon"], label="Used")
ax2.set_title(f"Resource Usage (Final Value: {final_value})", fontsize=16, fontweight="bold")
ax2.set_ylabel("Units", fontsize=12)
ax2.legend()

plt.tight_layout(w_pad=5.0, rect=[0, 0.03, 1, 0.95])
plt.suptitle("Genetic Algorithms - Knapsack Problem", fontsize=26, fontweight="bold")
plt.show()