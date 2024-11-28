import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from generator import Generator
import random
import copy
from stable import Stable

# Hàm vẽ hình các đối tượng trong không gian 3D
def draw_box(ax, origin, size, color):
    x, y, z = origin
    dx, dy, dz = size
    
    vertices = [
        [x, y, z],
        [x + dx, y, z],
        [x + dx, y + dy, z],
        [x, y + dy, z],
        [x, y, z + dz],
        [x + dx, y, z + dz],
        [x + dx, y + dy, z + dz],
        [x, y + dy, z + dz]
    ]

    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],
        [vertices[4], vertices[5], vertices[6], vertices[7]],
        [vertices[0], vertices[1], vertices[5], vertices[4]],
        [vertices[2], vertices[3], vertices[7], vertices[6]],
        [vertices[1], vertices[2], vertices[6], vertices[5]],
        [vertices[4], vertices[7], vertices[3], vertices[0]]
    ]
    
    ax.add_collection3d(Poly3DCollection(faces, facecolors=color, linewidths=1, edgecolors='r', alpha=.25))

def visual_plot(lst_box, size_bin):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    large_box = ((0, 0, 0), (size_bin[0], size_bin[1], size_bin[2]), 'cyan')
    draw_box(ax, *large_box)
    color = ['blue', 'green', 'red', 'purple', 'yellow', 'orange']

    for box in lst_box:
        origin = (box[0], box[1], box[2])
        size = (box[3], box[4], box[5])
        box_color = color[np.random.randint(0, len(color))]
        draw_box(ax, origin, size, box_color)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Bin Packing Visualization')

    ax.set_xlim(0, size_bin[0])
    ax.set_ylim(0, size_bin[1])
    ax.set_zlim(0, size_bin[2])

    plt.show()

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

# Lớp đại diện cho thùng chứa trong bài toán 3D Bin Packing
class Bin3D:
    def __init__(self, width, depth, height):
        self.width = width
        self.depth = depth
        self.height = height
        self.items = []

    def can_fit(self, item, position):
        x, y, z = position
        item_width, item_depth, item_height = item
        if (x + item_width <= self.width and
            y + item_depth <= self.depth and
            z + item_height <= self.height):

            tmp=np.zeros((self.width,self.depth,self.height),dtype=int) 

            for placed_item in self.items: 
                placed_pos, placed_dim = placed_item 
                px, py, pz = placed_pos
                pw, pd, ph = placed_dim
                if (x < px + pw and x + item_width > px and
                    y < py + pd and y + item_depth > py and
                    z < pz + ph and z + item_height > pz):
                    return False

                tmp[pz:pz+ph,px:px+pw,py:py+pd]=1
                  
            return Stable(tmp,item,x,y,z)
            return True
        return False

    def add_item_2(self, item, rotation_index):
        rotated_item = self.rotation(item[1], rotation_index)
        for z in range(self.height):
            for y in range(self.depth):
                for x in range(self.width):
                    if self.can_fit(rotated_item, (x, y, z)):
                        self.items.append(([x, y, z], rotated_item))
                        return True
        return False

    def rotation(self, item, type_rotation):
        W, L, H = item 
        if type_rotation == 0:
            return [W, L, H]
        elif type_rotation == 1:
            return [L, W, H]
        elif type_rotation == 2:
            return [W, H, L]
        elif type_rotation == 3:
            return [H, W, L]
        elif type_rotation == 4:
            return [H, L, W]
        elif type_rotation == 5:
            return [L, H, W]

    def __repr__(self):
        return f"Bin3D(items={self.items})"

# Hàm thực hiện chiến lược deep bottom-left bin packing
def deep_bottom_left_bin_packing_3d(items, bin_dimensions, rotation, individual):
    bins = []
    items = sorted(items, key=lambda x: x[1][0] * x[1][1] * x[1][2], reverse=True)


    for i, item in enumerate(items):
        placed = False
        for bin in bins:
            if bin.add_item_2(item, individual.cathe[i]):
                placed = True
                break 
        if not placed:
            new_bin = Bin3D(*bin_dimensions)
            new_bin.add_item_2(item, individual.cathe[i])
            bins.append(new_bin)
    return bins

# Hàm giải bài toán và trả về kết quả
def solve(data, individual, rotation, visualize=False):
    lst_items = data.items[0]
    bin_size = data.bin_size
    bins = deep_bottom_left_bin_packing_3d(lst_items, bin_size, rotation, individual)
    
    lst = []
    static = {'used_space': 0, 'num_packed': 0}
    for i in range(len(bins[0].items)):
        item = list(bins[0].items[i][0]) + list(bins[0].items[i][1])
        lst.append(item)
    static['used_space'] = sum([a[1][0] * a[1][1] * a[1][2] for a in bins[0].items]) / (bin_size[0] * bin_size[1] * bin_size[2])
    static['num_packed'] = len(bins[0].items)
    if visualize:
        visual_plot(lst, bin_size)

    return static['used_space']

# Thuật toán di truyền để giải bài toán
def ga(data, popsize, cr, mr):
    population = [Individual(n_items) for _ in range(popsize)]
    for individual in population:
        individual.create()

    for i in range(popsize):
        population = nextgen(data, population, popsize, cr, mr)
        print(i, solve(data, population[0], True))

    return population

if __name__ == '__main__':
    n_items = 30
    popsize = 10
    data = Generator(n_items, bin_size=[20, 20, 20], seed=4)
    data.generate()

    pop = ga(data, popsize, 0.8, 0.1)

    solve(data, pop[0], True, visualize=True)