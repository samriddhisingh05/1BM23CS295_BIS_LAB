import random

ROAD_LENGTH = 20
MAX_ITER = 10

road = [random.choice([0, 1]) for _ in range(ROAD_LENGTH)]
print("Initial Road State:", road)

for iter in range(1, MAX_ITER + 1):
new_road = [0] * ROAD_LENGTH

for i in range(ROAD_LENGTH):
next_cell = (i + 1) % ROAD_LENGTH

if road[i] == 1 and road[next_cell] == 0:
new_road[next_cell] = 1 # Car moves forward
elif road[i] == 1 and road[next_cell] == 1:
new_road[i] = 1 # Car stays (blocked)
else:
new_road[i] = new_road[i] or 0 # Empty remains empty
road = new_road.copy()

print(f"After iteration {iter}:", road)
