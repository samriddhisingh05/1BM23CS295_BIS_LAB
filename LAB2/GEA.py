import random

# Step 1: Define the Problem (optimization function)
def fitness_function(x):
    return x ** 2   # Example: maximize x^2

# Step 2: Initialize Parameters
POPULATION_SIZE = 10
CHROMOSOME_LENGTH = 8   # number of bits (genes)
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.7
GENERATIONS = 7


# Convert binary string to integer (Gene Expression: decoding)
def decode(chromosome):
    return int(chromosome, 2)

# Step 3: Initialize Population
def initialize_population():
    return [''.join(random.choice('01') for _ in range(CHROMOSOME_LENGTH)) 
            for _ in range(POPULATION_SIZE)]

# Step 4: Evaluate Fitness
def evaluate_population(population):
    return [fitness_function(decode(ind)) for ind in population]

# Step 5: Selection (Roulette Wheel)
def select(population, fitness):
    total_fit = sum(fitness)
    probs = [f / total_fit for f in fitness]
    chosen = random.choices(population, weights=probs, k=2)
    return chosen

# Step 6: Crossover
def crossover(p1, p2):
    if random.random() < CROSSOVER_RATE:
        point = random.randint(1, CHROMOSOME_LENGTH - 1)
        return p1[:point] + p2[point:], p2[:point] + p1[point:]
    return p1, p2

# Step 7: Mutation
def mutate(chromosome):
    return ''.join(
        bit if random.random() > MUTATION_RATE else random.choice('01')
        for bit in chromosome
    )

# Step 8: Gene Expression (already handled by decode in fitness function)

# Step 9 & 10: Iterate and Output Best Solution
def gene_expression_algorithm():
    population = initialize_population()
    
    for gen in range(GENERATIONS):
        fitness = evaluate_population(population)
        new_population = []
        
        # Track best solution
        best_idx = fitness.index(max(fitness))
        best_solution = population[best_idx]
        best_value = decode(best_solution)
        print(f"Gen {gen+1} | Best: {best_solution} (x={best_value}, f={fitness[best_idx]})")
        
        # Create new generation
        while len(new_population) < POPULATION_SIZE:
            p1, p2 = select(population, fitness)
            c1, c2 = crossover(p1, p2)
            c1, c2 = mutate(c1), mutate(c2)
            new_population.extend([c1, c2])
        
        population = new_population[:POPULATION_SIZE]
    
    # Final best
    fitness = evaluate_population(population)
    best_idx = fitness.index(max(fitness))
    best_solution = population[best_idx]
    print("\nBest Solution Found:")
    print(f"Chromosome: {best_solution}")
    print(f"x = {decode(best_solution)}, f(x) = {fitness[best_idx]}")

# Run Algorithm
gene_expression_algorithm()
