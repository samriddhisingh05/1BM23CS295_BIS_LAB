import random


def fitness_function(x):
    return x ** 2   


POPULATION_SIZE = 10
CHROMOSOME_LENGTH = 8  
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.7
GENERATIONS = 7

def decode(chromosome):
    return int(chromosome, 2)

def initialize_population():
    return [''.join(random.choice('01') for _ in range(CHROMOSOME_LENGTH)) 
            for _ in range(POPULATION_SIZE)]

def evaluate_population(population):
    return [fitness_function(decode(ind)) for ind in population]

def select(population, fitness):
    total_fit = sum(fitness)
    probs = [f / total_fit for f in fitness]
    chosen = random.choices(population, weights=probs, k=2)
    return chosen

def crossover(p1, p2):
    if random.random() < CROSSOVER_RATE:
        point = random.randint(1, CHROMOSOME_LENGTH - 1)
        return p1[:point] + p2[point:], p2[:point] + p1[point:]
    return p1, p2

def mutate(chromosome):
    return ''.join(
        bit if random.random() > MUTATION_RATE else random.choice('01')
        for bit in chromosome
    )

def gene_expression_algorithm():
    population = initialize_population()
    
    for gen in range(GENERATIONS):
        fitness = evaluate_population(population)
        new_population = []
        
        best_idx = fitness.index(max(fitness))
        best_solution = population[best_idx]
        best_value = decode(best_solution)
        print(f"Gen {gen+1} | Best: {best_solution} (x={best_value}, f={fitness[best_idx]})")
        
   
        while len(new_population) < POPULATION_SIZE:
            p1, p2 = select(population, fitness)
            c1, c2 = crossover(p1, p2)
            c1, c2 = mutate(c1), mutate(c2)
            new_population.extend([c1, c2])
        
        population = new_population[:POPULATION_SIZE]
    
 
    fitness = evaluate_population(population)
    best_idx = fitness.index(max(fitness))
    best_solution = population[best_idx]
    print("\nBest Solution Found:")
    print(f"Chromosome: {best_solution}")
    print(f"x = {decode(best_solution)}, f(x) = {fitness[best_idx]}")

gene_expression_algorithm()
