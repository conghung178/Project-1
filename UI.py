import tkinter as tk
from tkinter import ttk, messagebox
from GA import ga
from DBL import solve
import torch
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


# Đường dẫn đến file .pt của bạn
pt_file_path = 'D:/Project 1/cut_1-1.pt'
model = torch.load(pt_file_path, map_location=torch.device('cpu'))

# Tạo dữ liệu thủ công
class ManualData:
    def __init__(self, items, bin_size):
        self.items = [items]  # Danh sách các vật phẩm, tổ chức như `data.items`
        self.bin_size = bin_size  # Kích thước của thùng chứa
        self.filename = "manual_data.dat"
        self.total_volume = sum([dim[0] * dim[1] * dim[2] for _, dim in items])  # Tổng thể tích của các vật phẩm

def run_program():
    try:
        # Lấy giá trị i từ ô nhập
        i = int(entry_i.get())
        if i < 0 or i >= len(model):
            raise ValueError("Giá trị i không hợp lệ. Vui lòng nhập giá trị trong phạm vi hợp lệ.")

        # Kích thước các vật phẩm
        item_sizes = model[i]
        items = [([0, 0, 0], size) for size in item_sizes]
        bin_size = [10, 10, 10]

        # Tạo dữ liệu
        data = ManualData(items, bin_size)
        num_items = len(item_sizes)

        # Chạy GA
        popsize = 20
        pop = ga(num_items, data, popsize, 0.8, 0.1)
        result = solve(data, pop[0], True, visualize=True)

        # Hiển thị kết quả
        messagebox.showinfo("Kết quả", f"Tỷ lệ sử dụng không gian: {result * 100:.2f}%")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))


# Tạo giao diện
root = tk.Tk()
root.title("3D Bin Packing Problem")
root.geometry("1200x800")  # Đặt kích thước cửa sổ là 1200x800

# Label và Entry để nhập i
label_i = ttk.Label(root, text="Nhập i:")
label_i.grid(row=0, column=0, padx=10, pady=10)

entry_i = ttk.Entry(root)
entry_i.grid(row=0, column=1, padx=10, pady=10)

# Nút chạy chương trình
btn_run = ttk.Button(root, text="Chạy", command=run_program)
btn_run.grid(row=1, column=0, columnspan=2, pady=10)

# Chạy giao diện
root.mainloop()
