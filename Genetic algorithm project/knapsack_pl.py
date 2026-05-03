import random
import matplotlib.pyplot as plt
# KONFIGURACJA I DANE
POPULATION_SIZE = 50 # Liczba plecaków w jednym pokoleniu 
GENES_COUNT = 20 # Liczba dostępnych przedmiotów
GENERATIONS = 1000 # Liczba pokoleń
MUTATION_RATE = 0.05 # Szansa mutacji (5%)

MAX_WEIGHT = 50 # Limit wagi plecaka
MAX_WEAR = 30 # Limit zużycia plecaka (trzeci parametr)

# KONFIGURACJA PATIENCE
PATIENCE = 100
best_overall_fitness = 0
stagnation_counter = 0

# Generowanie losowych przedmiotów
items = [
    {"value": random.randint(10, 50),
     "weight": random.randint(1, 15),
     "wear": random.randint(1, 10)}
     for _ in range(GENES_COUNT)
]

# FUNKCJA FITNESS
def calculate_fitness(chromosome):
    total_value = 0
    total_weight = 0
    total_wear = 0

    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            total_value += items[i]["value"]
            total_weight += items[i]["weight"]
            total_wear += items[i]["wear"]


    # Przypadek przekroczenia limitu wagi lub zużycia
    if total_weight > MAX_WEIGHT or total_wear > MAX_WEAR:
        return 0
    
    return total_value

# OPERACJE GENETYCZNE
def create_population():
    return [[random.randint(0, 1) for _ in range(GENES_COUNT)] for _ in range(POPULATION_SIZE)] 
    
def crossover(parent1, parent2):
    # Krzyżowanie punktowe: bierzemy część genów od jednego i część od drugiego
    point = random.randint(1, GENES_COUNT - 1)
    child = parent1[:point] + parent2[point:]
    return child 

def mutate(chromosome):
    for i in range(len(chromosome)):
        if random.random() < MUTATION_RATE:
            chromosome[i] = 1 - chromosome[i]
    return chromosome

# GŁÓWNA PĘTLA ALGORYTMU
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
        print(f"--- STOP: Stagnacja w pokoleniu {gen}. Brak poprawy od {PATIENCE} generacji. ---")
        break


    if gen % 10 == 0:
        print(f"{gen:<5} | {best_fitness:<10} | Optymalizacja...")

    # Elitaryzm, tworząc nową populację zostawiamy dwa najlepszych osobnika
    new_population = population[:2] 

    while len(new_population) < POPULATION_SIZE:
        p1, p2 = random.sample(population[:POPULATION_SIZE // 2], 2)
        child = crossover(p1, p2)
        child = mutate(child)
        new_population.append(child)
        population = new_population
    
   


# WYŚWIETLENIE WYNIKÓW KOŃCOWYCH
best_backpack = population[0]
final_value = calculate_fitness(best_backpack)
final_weight = sum(items[i]["weight"] for i in range(GENES_COUNT) if best_backpack[i] == 1)
final_wear = sum(items[i]["wear"] for i in range(GENES_COUNT) if best_backpack[i] == 1)

print("-"*35)
print(f"NAJLEPSZY PLECAK PO {GENERATIONS} POKOLENIACH:")
print(f"Wartość: {final_value}")
print(f"Waga: {final_weight}/{MAX_WEIGHT}")
print(f"Zużycie: {final_wear}/{MAX_WEAR}")

# WYKRESY
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10))


# Wykres 1: Historia Fitness
ax1.plot(range(1, population_counter+1), best_local_backpacks)
ax1.set_title("Postęp ewolucjii (Wartość plecaka)", fontsize=16, fontweight="bold")
ax1.set_xlabel("Pokolenie", fontsize=12)
ax1.set_ylabel("Najlepsza wartość (Fitness)", fontsize=12)
ax1.grid(True)


# Wykres 2: Wykorzystanie limitów
labels = ["Waga", "Zużycie"]
current_values = [final_weight, final_wear]
max_values = [MAX_WEIGHT, MAX_WEAR]

ax2.bar(labels, max_values, color="lightgrey", label="Limit")
bars = ax2.bar(labels, current_values, color=["skyblue", "salmon"], label="Wykorzystano")
ax2.set_title(f"Wykorzystano zasobów (Finalna wartość): {final_value}", fontsize=16, fontweight="bold")
ax2.set_ylabel("Jednostki", fontsize=12)
ax2.legend()

plt.tight_layout(w_pad=5.0, rect=[0, 0.03, 1, 0.95])
plt.suptitle("Algorytmy genetyczne - problem plecaka", fontsize=26, fontweight="bold")
plt.show()



