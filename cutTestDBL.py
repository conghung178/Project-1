from GA import ga
from DBL import solve
import numpy as np
from GA import Individual

import torch

# Đọc file .pt chứa dữ liệu
pt_file_path = r'D:\Project 1\cut_1-1.pt'  # Đường dẫn đến file .pt của bạn
model = torch.load(pt_file_path, map_location=torch.device('cpu'))

# Nhập i
i = int(input("Nhập i: ")) 
# Kích thước các vật phẩm đã cho
item_sizes = model[i]

# Thêm tọa độ gốc (mặc định là [0, 0, 0])
items = [([0, 0, 0], size) for size in item_sizes]

# Kích thước của thùng chứa
bin_size = [10, 10, 10]

# Tạo đối tượng tương tự như `Generator`
class ManualData:
    def __init__(self, items, bin_size):
        self.items = [items]  # Danh sách các vật phẩm, tổ chức như `data.items`
        self.bin_size = bin_size  # Kích thước của thùng chứa
        self.filename = "manual_data.dat"
        self.total_volume = sum([dim[0] * dim[1] * dim[2] for _, dim in items])  # Tổng thể tích của các vật phẩm

# Tạo dữ liệu thủ công
data = ManualData(items, bin_size)

# Đếm số lượng vật phẩm trong danh sách
num_items = len(item_sizes)

if __name__ == '__main__':
    popsize = 20
    print(model[i])
    
    individual = Individual(num_items)
    individual.cathe = np.zeros(num_items, dtype=int)  # Gán tất cả kiểu xoay = 0

    result = solve(data, individual, True, visualize=True)

    print("Tỷ lệ phủ của thùng là:", result)