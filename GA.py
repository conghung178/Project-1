
import random
import copy
import numpy as np

# Lớp đại diện cho một cá thể trong thuật toán di truyền
class Individual:
    def __init__(self, sothung):
        self.sothung = sothung
        self.cathe = np.zeros(self.sothung, dtype=int)

    # Khởi tạo ngẫu nhiên kiểu xoay của các vật phẩm
    def create(self):
        for i in range(self.sothung):
            self.cathe[i] = random.randint(0, 5)

# Hàm lai ghép giữa hai cá thể
def crossover(p1, p2):
    n = p1.sothung # số lượng vật phẩm
    i = random.randint(0, n) # điểm cắt ngẫu nhiên

    c1 = Individual(n)
    c2 = Individual(n)
    # Lai ghép các cá thể, tạo ra 2 cá thể con 
    # Kết hợp nửa đầu từ cha và nửa sau từ mẹ để tạo ra cá thể con.
    c1.cathe = np.concatenate((p1.cathe[:i], p2.cathe[i:]))
    c2.cathe = np.concatenate((p2.cathe[:i], p1.cathe[i:]))
    return c1, c2

# Hàm đột biến một cá thể
def mutate(p):
    n = p.sothung
    child = copy.deepcopy(p)
    # Chọn ngẫu nhiên một vị trí trong cá thể và thay đổi kiểu xoay của nó
    point = random.randint(0, n-1)
    # Thay đổi kiểu xoay của vật phẩm tại vị trí point
    child.cathe[point] = random.randint(0, 5)  # Thay đổi giá trị bằng số ngẫu nhiên giữa 0 và 5
    return child

# Hàm để tạo thế hệ mới từ quần thể hiện tại
def nextgen(data, population, popsize, cr, mr):
    '''
    data: Dữ liệu đầu vào của bài toán.
    population: Quần thể hiện tại (danh sách các cá thể).
    popsize: Số lượng cá thể trong quần thể.
    cr: Xác suất lai ghép (crossover rate).
    mr: Xác suất đột biến (mutation rate).
    '''
    from DBL import solve

    # khởi tạo một danh sách thế hệ mới
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