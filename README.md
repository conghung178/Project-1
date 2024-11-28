# Project 1: Bài toán đóng gói thùng hàng với chi phí tối thiểu

## Giới thiệu

**Bin Packing Problem** (Bài toán Đóng gói thùng) là một bài toán tối ưu hóa cổ điển trong lĩnh vực khoa học máy tính và toán học. Mục tiêu của bài toán này là phân loại một tập hợp các đối tượng (items) vào các thùng (bins) sao cho số thùng sử dụng là tối thiểu, với mỗi thùng có một dung lượng cố định. Bài toán này có rất nhiều ứng dụng thực tiễn, chẳng hạn như trong việc tối ưu hóa không gian lưu trữ, tối ưu hóa vận tải hoặc phân phối tài nguyên.

Dự án này cung cấp giải pháp cho bài toán Bin Packing, sử dụng các thuật toán khác nhau như **First-Fit**, **Best-Fit**, **Worst-Fit**, **phương pháp heuristics**, **giải thuật di truyền** để tìm ra cách đóng gói tối ưu nhất.

## Mục tiêu

Mục tiêu của dự án là cung cấp một giải pháp cho bài toán Bin Packing, giúp giảm thiểu số lượng thùng cần sử dụng khi phân loại các đối tượng có kích thước khác nhau. Thực hiện xếp thùng hàng sao cho thỏa mãn các điều kiện thực tế như điều kiện vật lý, điều kiện cân bằng. Dự án này có thể áp dụng trong nhiều lĩnh vực như:

- **Tối ưu hóa không gian lưu trữ**: Giúp các công ty giảm thiểu không gian lưu trữ khi đóng gói các sản phẩm.
- **Tối ưu hóa vận tải**: Tối ưu hóa việc vận chuyển hàng hóa bằng cách phân bổ các gói hàng vào các thùng sao cho số thùng cần sử dụng là ít nhất.
- **Phân phối tài nguyên**: Trong môi trường điện toán phân tán, bài toán này có thể giúp tối ưu hóa việc phân phối tài nguyên vào các máy chủ.

## Các tính năng chính

- **Thuật toán First-Fit (FF)**: Chạy qua các đối tượng và đóng gói chúng vào thùng đầu tiên có thể chứa được chúng.
- **Thuật toán Best-Fit (BF)**: Chọn thùng có thể chứa đối tượng nhưng lại "chật" nhất, giúp tối ưu hóa không gian.
- **Thuật toán Worst-Fit (WF)**: Chọn thùng có không gian dư thừa lớn nhất.
- **Heuristic Algorithms**: Áp dụng các thuật toán heuristic để cải thiện hiệu suất đóng gói với ít thùng hơn, cụ thể ở đây sử dụng thuật toán **deep-bottom-left (DBL)**.
- **Giải thuật di truyền**: Áp dụng thuật toán di truyền để tối ưu hóa không gian, hỗ trợ tính năng xoay thùng hàng để thu được cách xếp thùng hàng tối ưu nhất.
- **Phân tích hiệu suất**: Đánh giá hiệu quả của các thuật toán dựa trên số lượng thùng đã sử dụng và thời gian chạy của thuật toán dựa trên độ phủ kín của thùng. 

## Công nghệ sử dụng

- **Ngôn ngữ lập trình**: Python
- **Thư viện**: 
  - `numpy` (để tính toán các phép toán số học và ma trận)
  - `matplotlib` (để vẽ đồ thị và trực quan hóa kết quả)
  - `time` (để đo thời gian chạy của các thuật toán)
- **Framework**: Không sử dụng framework đặc biệt (đây là một bài toán thuật toán đơn giản).
