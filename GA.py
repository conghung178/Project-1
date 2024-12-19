
import random
import copy
import numpy as np

# Lớp đại diện cho một cá thể trong thuật toán di truyền
class Individual:
    def __init__(self, sothung):
        self.sothung = sothung
        self.cathe = np.zeros(self.sothung, dtype=int)

    def create(self):
        for i in range(self.sothung):
            self.cathe[i] = random.randint(0, 5)

# Hàm lai ghép giữa hai cá thể
def crossover(p1, p2):
    n = p1.sothung
    i = random.randint(0, n)

    c1 = Individual(n)
    c2 = Individual(n)
    c1.cathe = np.concatenate((p1.cathe[:i], p2.cathe[i:]))
    c2.cathe = np.concatenate((p2.cathe[:i], p1.cathe[i:]))
    return c1, c2

# Hàm đột biến một cá thể
def mutate(p):
    n = p.sothung
    child = copy.deepcopy(p)
    point = random.randint(0, n-1)
    child.cathe[point] = random.randint(0, 5)  # Thay đổi giá trị bằng số ngẫu nhiên giữa 0 và 5
    return child

# Hàm để tạo thế hệ mới
def nextgen(data, population, popsize, cr, mr):
    from DBL import solve
    k = 0
    child = population.copy()
    while k < popsize:
        parent1 = random.choice(population)
        parent2 = random.choice(population)

        if random.random() < cr:
            child1, child2 = crossover(parent1, parent2)
            if child1 not in child:
                child.append(child1)
                k += 1
            if child2 not in child:
                child.append(child2)
                k += 1

        if random.random() < mr:
            child1 = mutate(parent1)
            child2 = mutate(parent2)
            if child1 not in child:
                child.append(child1)
                k += 1
            if child2 not in child:
                child.append(child2)
                k += 1

    child.sort(key=lambda x: solve(data, x, True), reverse=True)
    return child[:popsize]

# Thuật toán di truyền để giải bài toán
def ga(n_items,data, popsize, cr, mr):
    from DBL import solve
    population = [Individual(n_items) for _ in range(popsize)]
    for individual in population:
        individual.create()

    for i in range(popsize):
        population = nextgen(data, population, popsize, cr, mr)
        print(i, solve(data, population[0], True))

    return population