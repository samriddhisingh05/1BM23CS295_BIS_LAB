import numpy as np
import matplotlib.pyplot as plt


def objective_function(x):
    return x**2 - 4*x + 4

class Particle:
    def __init__(self, lower_bound, upper_bound):
        self.position = np.random.uniform(lower_bound, upper_bound)  
        self.velocity = np.random.uniform(-1, 1)  
        self.best_position = self.position
        self.best_value = objective_function(self.position)

    def update(self, global_best_position, w, c1, c2):
        r1 = np.random.rand()  
        r2 = np.random.rand()  

        
        self.velocity = w * self.velocity + c1 * r1 * (self.best_position - self.position) + c2 * r2 * (global_best_position - self.position)
        self.position += self.velocity

        
        current_value = objective_function(self.position)

        
        if current_value < self.best_value:
            self.best_value = current_value
            self.best_position = self.position

# PSO parameters
num_particles = 30
num_iterations = 100
w = 0.7  
c1 = 1.5 
c2 = 1.5  
lower_bound = -10  
upper_bound = 10  


particles = [Particle(lower_bound, upper_bound) for _ in range(num_particles)]


global_best_position = particles[0].best_position
global_best_value = particles[0].best_value

# PSO loop
for iteration in range(num_iterations):
    for particle in particles:
        particle.update(global_best_position, w, c1, c2)

        
        if particle.best_value < global_best_value:
            global_best_value = particle.best_value
            global_best_position = particle.best_position

    
    if iteration % 10 == 0:
        print(f"Iteration {iteration}: Global Best Position = {global_best_position}, Value = {global_best_value}")


print(f"\nOptimal Position: {global_best_position}")
print(f"Optimal Value: {global_best_value}")


x_values = np.linspace(lower_bound, upper_bound, 100)
y_values = objective_function(x_values)

plt.plot(x_values, y_values, label="Objective Function f(x)")
plt.scatter(global_best_position, global_best_value, color='red', label='Optimal Solution (PSO)', zorder=5)
plt.title("Particle Swarm Optimization for Minimizing f(x) = x^2 - 4x + 4")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.show()
