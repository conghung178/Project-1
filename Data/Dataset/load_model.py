import torch

# Tải mô hình từ file .pt
model = torch.load('D:\Project 1\cut_1-1.pt')

# Đảm bảo rằng mô hình ở chế độ evaluation (eval) nếu bạn muốn sử dụng mô hình cho inference
model.eval()

# Sử dụng mô hình cho các tác vụ như dự đoán (inference)
# Ví dụ: outputs = model(inputs)
