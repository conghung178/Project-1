from visual import visual_plot
import numpy as np
from generator import Generator
from stable import Stable
from GA import ga

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


if __name__ == '__main__':
    n_items = 30
    popsize = 10
    data = Generator(n_items, bin_size=[20, 20, 20], seed=4)
    data.generate()

    pop = ga(n_items,data, popsize, 0.8, 0.1)

    solve(data, pop[0], True, visualize=True)