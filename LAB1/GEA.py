import random
import math

def target_function(x):
    return x * math.sin(10 * math.pi * x) + 1.0

POPULATION_SIZE = 50
GENE_LENGTH = 10
GENERATIONS = 7   # Only 7 generations
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.7
DOMAIN = (-1, 1)
FUNCTIONS = {
    "add": (lambda a, b: a + b, "+"),
    "sub": (lambda a, b: a - b, "-"),
    "mul": (lambda a, b: a * b, "*"),
    "div": (lambda a, b: a / b if b != 0 else 1, "/")
}
TERMINALS = ['x', 1.0, -1.0, 2.0]

def random_gene():
    gene = []
    for _ in range(GENE_LENGTH):
        if random.random() < 0.5:
            gene.append(random.choice(list(FUNCTIONS.keys())))
        else:
            gene.append(random.choice(TERMINALS))
    return gene

population = [random_gene() for _ in range(POPULATION_SIZE)]

def evaluate_gene(gene, x):
    stack = []
    for g in gene:
        if g in TERMINALS:
            stack.append(x if g == 'x' else g)
        elif g in FUNCTIONS:
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                stack.append(FUNCTIONS[g][0](a, b))
    return stack[0] if stack else 0


def fitness(gene):
    total_error = 0.0
    for _ in range(10):
        x = random.uniform(*DOMAIN)
        try:
            y_pred = evaluate_gene(gene, x)
        except:
            y_pred = 0
        y_true = target_function(x)
        total_error += abs(y_true - y_pred)
    return 1 / (1 + total_error)


def select(pop):
    k = 3
    candidates = random.sample(pop, k)
    return max(candidates, key=lambda g: fitness(g))

def crossover(parent1, parent2):
    if random.random() < CROSSOVER_RATE:
        point = random.randint(1, GENE_LENGTH - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1[:], parent2[:]

def mutate(gene):
    for i in range(GENE_LENGTH):
        if random.random() < MUTATION_RATE:
            if random.random() < 0.5:
                gene[i] = random.choice(list(FUNCTIONS.keys()))
            else:
                gene[i] = random.choice(TERMINALS)
    return gene

def gene_to_expression(gene):
    stack = []
    for g in gene:
        if g in TERMINALS:
            stack.append(str(g))
        elif g in FUNCTIONS:
            if len(stack) >= 2:
                b = stack.pop()
                a = stack.pop()
                op = FUNCTIONS[g][1]
                stack.append(f"({a} {op} {b})")
    return stack[0] if stack else "0"

best_gene = None
best_fit = -float("inf")

for gen in range(GENERATIONS):
    new_population = []
    while len(new_population) < POPULATION_SIZE:
        p1 = select(population)
        p2 = select(population)
        c1, c2 = crossover(p1, p2)
        c1 = mutate(c1)
        c2 = mutate(c2)
        new_population.extend([c1, c2])

    population = new_population[:POPULATION_SIZE]

    # Track best solution
    for gene in population:
        f = fitness(gene)
        if f > best_fit:
            best_fit = f
            best_gene = gene

    print(f"Generation {gen+1}: Best Fitness = {best_fit:.5f}")

print("\nBest Gene (raw):")
print(" ".join(map(str, best_gene)))
print("Best Gene (expression):")
print(gene_to_expression(best_gene))
print("Best Fitness:", best_fit)
