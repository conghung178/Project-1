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
    
    #Chức năng: kiểm tra xem một vật có thể đặt được vào thùng tại vị trí (x, y, z) hay không
    #đảm bảo vật không bị tràn ra ngoài giới hạn ba chiều của thùng
    def can_fit(self, item, position):
        x, y, z = position
        item_width, item_depth, item_height = item
        if (x + item_width <= self.width and
            y + item_depth <= self.depth and
            z + item_height <= self.height):

            tmp=np.zeros((self.width,self.depth,self.height),dtype=int) #Tạo một mảng 3D để lưu trữ vị trí các vật đã được đặt vào thùng

            #Chức năng: Duyệt qua các vật đã được đặt vào thùng
            #so sánh vị trí của vật cần đặt với từng vật đã được đặt
            for placed_item in self.items: 
                placed_pos, placed_dim = placed_item 
                px, py, pz = placed_pos
                pw, pd, ph = placed_dim
                if (x < px + pw and x + item_width > px and
                    y < py + pd and y + item_depth > py and
                    z < pz + ph and z + item_height > pz):
                    return False

                tmp[pz:pz+ph,px:px+pw,py:py+pd]=1
                  
            return Stable(tmp,item,x,y,z) #Kiem tra tinh on dinh vật lý cua vat
        return False

    #Chức năng: thêm một vật vào thùng chứa nếu tìm được vị trí phù hợp
    def add_item(self, item, rotation_index):
        #item: vật cần xếp: 6 tham số
        rotated_item = self.rotation(item[1], rotation_index) # kích thước của vật sau khi xoay

        #duyệt không gian trong thùng qua từng vị trí (x, y, z)
        for z in range(self.height):
            for y in range(self.depth):
                for x in range(self.width):
                    if self.can_fit(rotated_item, (x, y, z)):
                        self.items.append(([x, y, z], rotated_item)) #Thêm vật vào thùng theo chiến lược DBL
                        return True
        return False #Không tìm được vị trí phù hợp thì trả về False

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

    #Hàm hiển thị thông tin danh sách các vật đã được đặt vào thùng
    def __repr__(self):
        return f"Bin3D(items={self.items})"

# Hàm thực hiện chiến lược deep bottom-left bin packing
def deep_bottom_left_bin_packing_3d(items, bin_dimensions, rotation, individual):
    bins = [] # Khởi tạo danh sách các thùng rỗng để lưu trữ các thùng đã được đóng gói
    # Sắp xếp các vật phẩm theo thứ tự giảm dần của thể tích
    items = sorted(items, key=lambda x: x[1][0] * x[1][1] * x[1][2], reverse=True)

    # Duyệt qua từng vật phẩm
    for i, item in enumerate(items):
        placed = False
        for bin in bins:
            if bin.add_item(item, individual.cathe[i]):
                placed = True
                break 
        if not placed:
            new_bin = Bin3D(*bin_dimensions)
            new_bin.add_item(item, individual.cathe[i])
            bins.append(new_bin)
    return bins

# Hàm giải bài toán và trả về kết quả
#individual: cá thể tốt nhất sau khi chạy thuật toán GA, mỗi phần tử trong cá thể là một số nguyên từ 0 đến 5
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