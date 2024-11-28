import tkinter as tk
from tkinter import ttk
import threading
import time
from DBL import solve, ga, deep_bottom_left_bin_packing_3d, Bin3D, Individual
from generator import Generator

class BinPackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Giao diện đóng gói thùng 3D")

        # Nhập số lượng vật phẩm
        self.label_items = tk.Label(root, text="Số lượng vật phẩm:")
        self.label_items.grid(row=0, column=0, padx=10, pady=10)
        self.entry_items = tk.Entry(root, width=10)
        self.entry_items.grid(row=0, column=1)
        self.entry_items.insert(0, "30")  # Giá trị mặc định

        # Nhập kích thước thùng
        self.label_size = tk.Label(root, text="Kích thước thùng (DxRxC):")
        self.label_size.grid(row=1, column=0, padx=10, pady=10)

        self.entry_width = tk.Entry(root, width=5)
        self.entry_width.grid(row=1, column=1)
        self.entry_width.insert(0, "100")

        self.entry_depth = tk.Entry(root, width=5)
        self.entry_depth.grid(row=1, column=2)
        self.entry_depth.insert(0, "100")

        self.entry_height = tk.Entry(root, width=5)
        self.entry_height.grid(row=1, column=3)
        self.entry_height.insert(0, "100")

        # Thanh trạng thái tải
        self.progress = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
        self.progress.grid(row=2, column=0, columnspan=4, pady=10)

        # Nút "Chạy"
        self.run_button = tk.Button(root, text="Chạy", command=self.run_simulation)
        self.run_button.grid(row=3, column=0, columnspan=4, pady=10)

        # Kết quả
        self.label_result = tk.Label(root, text="", font=("Arial", 12))
        self.label_result.grid(row=4, column=0, columnspan=4, pady=10)

    def run_progress_bar(self):
        # Thanh trạng thái tải chạy từ 0 đến 100 trong 10 giây
        for i in range(101):
            self.progress['value'] = i
            self.root.update_idletasks()
            time.sleep(0.1)  # Thời gian giữa các bước là 0.1 giây (tổng 10 giây)

    def run_simulation(self):
        # Đọc số lượng vật phẩm và kích thước thùng từ giao diện
        n_items = int(self.entry_items.get())
        width = int(self.entry_width.get())
        depth = int(self.entry_depth.get())
        height = int(self.entry_height.get())

        # Tạo dữ liệu vật phẩm và thùng
        data = Generator(n_items, bin_size=[width, depth, height], seed = 4)
        data.generate()
        pop = ga(data, popsize, 0.8, 0.1)

        # Tạo luồng chạy thanh trạng thái và tính toán kết quả
        threading.Thread(target=self.run_progress_bar).start()

        # Gọi hàm solve từ DBL.py để tính toán
        result = solve(data, pop[0], True, visualize=True)

        # Số lượng thùng cần thiết và kích thước thùng
        num_bins = len(result[0])  # Số thùng cần thiết
        bin_size = f"{width} x {depth} x {height}"

        # Hiển thị kết quả
        result_text = f"Số thùng cần thiết: {num_bins}\nKích thước thùng: {bin_size}\nKết quả: {result}"
        self.label_result.config(text=result_text)

# Tạo cửa sổ giao diện
root = tk.Tk()
app = BinPackingApp(root)
root.mainloop()
