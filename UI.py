import tkinter as tk
from tkinter import ttk
from GA import ga
from DBL import solve
import torch
import threading


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

# Hàm hiển thị nội dung vào Label widget
def display_result(label_widget, result):
    label_widget.config(text=result)

# Hàm chạy chương trình
def run_program():
    try:
        display_result(result_label, "Đang tính toán...")

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
        best_individual = pop[0]

        # Giải bài toán để lấy tỷ lệ sử dụng
        result = solve(data, best_individual, True, visualize=False)

        # Hiển thị kết quả tỷ lệ sử dụng ngay lập tức
        display_result(result_label, f"Tỷ lệ sử dụng không gian: {result * 100:.2f}%")

        # Hiển thị trực quan trong một luồng riêng
        threading.Thread(target=solve, args=(data, best_individual, True, True)).start()

    except Exception as e:
        # Hiển thị lỗi trong Label kết quả
        display_result(result_label, f"Lỗi: {str(e)}")

# Tạo giao diện
root = tk.Tk()
root.title("3D Bin Packing Problem")
root.geometry("1200x800")  # Đặt kích thước cửa sổ là 1200x800

# Label và Entry để nhập i
label_i = ttk.Label(root, text="Nhập i:", font=("Arial", 14))
label_i.grid(row=0, column=0, padx=5, pady=10)

entry_i = ttk.Entry(root, font=("Arial", 14))
entry_i.grid(row=0, column=1, padx=10, pady=10)

# Nút chạy chương trình
btn_run = ttk.Button(root, text="Chạy", command=run_program)
btn_run.grid(row=1, column=0, columnspan=2, pady=10)

# Label để hiển thị kết quả
result_label = ttk.Label(root, text="Tỷ lệ sử dụng không gian: ", font=("Arial", 14))
result_label.grid(row=2, column=0, columnspan=2, pady=10)

# Chạy giao diện
root.mainloop()