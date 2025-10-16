import numpy as np
import random

cities = np.array([
    [0, 0],
    [1, 2],
    [3, 1],
    [5, 3],
    [6, 6],
])

print("define cities -")
for city in cities:
    print(f"[{city[0]},{city[1]}],")
print()

class AntColony:
    def __init__(self, cities, n_ants, n_iterations, alpha=1, beta=2, rho=0.1, q=100):
        self.cities = cities
        self.n_cities = len(cities)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.q = q
        self.pheromone = np.ones((self.n_cities, self.n_cities))
        self.distances = self.calculate_distances()

    def calculate_distances(self):
        distances = np.zeros((self.n_cities, self.n_cities))
        for i in range(self.n_cities):
            for j in range(i + 1, self.n_cities):
                dist = np.linalg.norm(self.cities[i] - self.cities[j])
                distances[i][j] = dist
                distances[j][i] = dist
        return distances

    def select_next_city(self, current_city, visited_cities):
        probabilities = []
        for next_city in range(self.n_cities):
            if next_city not in visited_cities:
                pheromone = self.pheromone[current_city][next_city] ** self.alpha
                distance = self.distances[current_city][next_city] ** -self.beta
                probabilities.append(pheromone * distance)
            else:
                probabilities.append(0)
        total_prob = sum(probabilities)
        probabilities = [p / total_prob for p in probabilities]
        return np.random.choice(range(self.n_cities), p=probabilities)

    def update_pheromone(self, ant_paths, ant_lengths):
        self.pheromone *= (1 - self.rho)
        for i, path in enumerate(ant_paths):
            for j in range(len(path) - 1):
                self.pheromone[path[j]][path[j + 1]] += self.q / ant_lengths[i]
            self.pheromone[path[-1]][path[0]] += self.q / ant_lengths[i]

    def optimize(self):
        shortest_path = None
        shortest_length = float('inf')

        for iteration in range(1, self.n_iterations + 1):
            ant_paths = []
            ant_lengths = []

            for _ in range(self.n_ants):
                path = [random.randint(0, self.n_cities - 1)]
                visited_cities = set(path)
                for _ in range(self.n_cities - 1):
                    current_city = path[-1]
                    next_city = self.select_next_city(current_city, visited_cities)
                    path.append(next_city)
                    visited_cities.add(next_city)
                path_length = sum(self.distances[path[i], path[i + 1]] for i in range(self.n_cities - 1))
                path_length += self.distances[path[-1], path[0]]
                ant_paths.append(path)
                ant_lengths.append(path_length)
                if path_length < shortest_length:
                    shortest_length = path_length
                    shortest_path = path
            self.update_pheromone(ant_paths, ant_lengths)
            print(f"Iteration {iteration} : Best path length = {shortest_length:.4f}")

        return shortest_path, shortest_length


n_ants = 10
n_iterations = 20
alpha = 1
beta = 2
rho = 0.1
q = 100

aco = AntColony(cities, n_ants, n_iterations, alpha, beta, rho, q)
best_path, best_length = aco.optimize()

print(f"\nBest path found : {best_path}")
print(f"Total distance of best path : {best_length:.4f}")
