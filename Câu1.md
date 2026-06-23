# 📘 TÀI LIỆU GIẢI THÍCH VÀ HƯỚNG DẪN TỰ CODE

# THUẬT TOÁN XỬ LÝ HISTOGRAM ẢNH

> **Mục đích:** Tài liệu này giúp người đọc hiểu rõ bản chất toán học của Histogram, Histogram Equalization và Histogram Stretching. Sau khi đọc xong, người đọc có thể tự cài đặt lại toàn bộ chương trình từ đầu mà không cần tham khảo code mẫu.

---

# MỤC LỤC

1. Đề bài
2. Histogram là gì?
3. Bước 1 – Đọc ảnh
4. Bước 2 – Chuyển ảnh sang ảnh xám
5. Bước 3 – Tính Histogram gốc (H1)
6. Bước 4 – Histogram Equalization
7. Bước 5 – Histogram sau cân bằng (H2)
8. Bước 6 – Histogram Stretching về khoảng [30,120]
9. Bước 7 – Histogram sau Stretch (H3)
10. Ví dụ tính tay đầy đủ
11. Quy trình xử lý toàn bộ chương trình
12. Hướng dẫn tự code lại
13. Độ phức tạp thuật toán
14. Kết luận

---

# 1. ĐỀ BÀI

Cho tập ảnh màu RGB trong thư mục đầu vào.

Yêu cầu:

* Chuyển ảnh sang ảnh xám.
* Tính Histogram gốc H1.
* Thực hiện Histogram Equalization.
* Tính Histogram sau cân bằng H2.
* Hiệu chỉnh mức xám về khoảng [30,120].
* Tính Histogram sau hiệu chỉnh H3.
* Hiển thị và lưu toàn bộ kết quả.

Chương trình phải tự động xử lý nhiều ảnh trong thư mục và lưu kết quả theo tên ảnh đầu vào.

---

# 2. HISTOGRAM LÀ GÌ?

Histogram là biểu đồ thể hiện sự phân bố mức xám của ảnh.

Đối với ảnh xám 8-bit:

* Mức xám nhỏ nhất: 0 (đen hoàn toàn)
* Mức xám lớn nhất: 255 (trắng hoàn toàn)

Histogram gồm:

```text
256 cột
0 → 255
```

Mỗi cột cho biết:

> Có bao nhiêu pixel trong ảnh mang mức xám tương ứng.

Ví dụ:

| Mức xám | Số pixel |
| ------- | -------- |
| 0       | 150      |
| 1       | 90       |
| 2       | 120      |
| ...     | ...      |
| 255     | 80       |

Nếu phần lớn pixel tập trung ở vùng thấp:

```text
0 → 80
```

ảnh sẽ tối.

Nếu phần lớn pixel tập trung ở vùng cao:

```text
180 → 255
```

ảnh sẽ sáng.

Nếu Histogram trải đều toàn khoảng:

```text
0 → 255
```

ảnh thường có độ tương phản tốt hơn.

---

# 3. BƯỚC 1 – ĐỌC ẢNH

Ảnh đầu vào được đọc bằng OpenCV:

```python
img = cv2.imread(image_path)
```

Kết quả:

```text
Ảnh RGB
↓
Ma trận kích thước H × W × 3
```

Trong đó:

* H: số hàng
* W: số cột
* 3: số kênh màu B, G, R

---

# 4. BƯỚC 2 – CHUYỂN ẢNH SANG ẢNH XÁM

## Tại sao phải chuyển ảnh xám?

Histogram trong bài toán này được tính trên cường độ sáng.

Do đó mỗi pixel chỉ cần một giá trị duy nhất thay vì 3 giá trị màu.

---

## Công thức chuyển đổi

Theo chuẩn ITU-R BT.601:

[
Gray = 0.299R + 0.587G + 0.114B
]

Trong OpenCV:

```python
gray = cv2.cvtColor(
    img,
    cv2.COLOR_BGR2GRAY
)
```

---

## Ý nghĩa

Mắt người nhạy với màu xanh lá nhất.

Do đó:

```text
G → trọng số lớn nhất
R → trung bình
B → nhỏ nhất
```

Kết quả:

```text
Ảnh màu RGB
↓
Ảnh xám
```

---

# 5. BƯỚC 3 – TÍNH HISTOGRAM GỐC (H1)

## Khởi tạo Histogram

Histogram có:

```python
H1 = np.zeros(256)
```

Mỗi phần tử:

```text
H1[i]
```

lưu số lượng pixel mang mức xám i.

---

## Thuật toán

Duyệt toàn bộ ảnh:

```python
for y in range(H):
    for x in range(W):
        H1[gray[y,x]] += 1
```

---

## Ý nghĩa

Ví dụ:

```text
Mức xám 100 xuất hiện 250 lần
```

thì:

```python
H1[100] = 250
```

---

# 6. BƯỚC 4 – HISTOGRAM EQUALIZATION

## Mục tiêu

Tăng độ tương phản của ảnh.

Histogram ban đầu thường chỉ tập trung trong một vùng nhỏ:

```text
50 → 120
```

Điều này làm ảnh thiếu chi tiết.

Histogram Equalization giúp phân bố lại mức xám trên toàn khoảng:

```text
0 → 255
```

---

## Bước 1: Tính PDF

PDF:

Probability Density Function

[
PDF(k)=\frac{H1(k)}{H\times W}
]

Trong code:

```python
pdf = H1/(H*W)
```

---

## Bước 2: Tính CDF

CDF:

Cumulative Distribution Function

[
CDF(k)=\sum_{i=0}^{k} PDF(i)
]

Trong code:

```python
cdf = np.cumsum(pdf)
```

---

## Bước 3: Hàm ánh xạ

[
s(k)=round(CDF(k)\times255)
]

Trong code:

```python
transform =
np.round(cdf*255)
```

---

## Bước 4: Sinh ảnh mới

```python
equalized = transform[gray]
```

Ý nghĩa:

```text
Mức xám cũ
↓
Mức xám mới
```

---

# 7. BƯỚC 5 – HISTOGRAM SAU CÂN BẰNG (H2)

Sau khi Equalization, tiếp tục tính Histogram mới:

```python
H2 = np.zeros(256)
```

Thuật toán tương tự H1.

Mục đích:

Đánh giá hiệu quả của Histogram Equalization.

Thông thường:

```text
H2 trải đều hơn H1
```

---

# 8. BƯỚC 6 – HISTOGRAM STRETCHING [30,120]

## Mục tiêu

Thay vì sử dụng toàn bộ khoảng:

```text
0 → 255
```

ta giới hạn mức xám về:

```text
30 → 120
```

---

## Công thức

[
new =
30 +
\frac{old}{255}
(120-30)
]

Trong code:

```python
stretch =
30 +
(equalized/255)*(120-30)
```

---

## Ý nghĩa

Nếu:

```text
old = 0
```

thì:

```text
new = 30
```

Nếu:

```text
old = 255
```

thì:

```text
new = 120
```

Toàn bộ mức xám được ánh xạ vào:

```text
[30,120]
```

---

# 9. BƯỚC 7 – HISTOGRAM SAU STRETCH (H3)

Histogram cuối cùng được tính từ ảnh Stretch.

Mục tiêu:

Kiểm tra xem toàn bộ mức xám đã được giới hạn trong:

```text
30 → 120
```

hay chưa.

---

# 10. VÍ DỤ TÍNH TAY ĐẦY ĐỦ

Giả sử Histogram:

| Mức xám | Số pixel |
| ------- | -------- |
| 0       | 2        |
| 1       | 3        |
| 2       | 5        |

Tổng số pixel:

[
N=10
]

PDF:

[
[0.2,;0.3,;0.5]
]

CDF:

[
[0.2,;0.5,;1.0]
]

Ánh xạ:

[
0\rightarrow51
]

[
1\rightarrow128
]

[
2\rightarrow255
]

Đây chính là nguyên lý hoạt động của Histogram Equalization.

---

# 11. QUY TRÌNH XỬ LÝ TOÀN BỘ CHƯƠNG TRÌNH

```text
Ảnh màu RGB
      ↓
Chuyển ảnh xám
      ↓
Histogram H1
      ↓
Histogram Equalization
      ↓
Histogram H2
      ↓
Stretch [30,120]
      ↓
Histogram H3
      ↓
Hiển thị kết quả
      ↓
Lưu output
```

---

# 12. HƯỚNG DẪN TỰ CODE LẠI

Bước 1:
Đọc ảnh.

Bước 2:
Chuyển ảnh sang ảnh xám.

Bước 3:
Khởi tạo H1.

Bước 4:
Duyệt toàn bộ pixel để tính Histogram.

Bước 5:
Tính PDF.

Bước 6:
Tính CDF.

Bước 7:
Tạo hàm ánh xạ Equalization.

Bước 8:
Sinh ảnh Equalized.

Bước 9:
Tính H2.

Bước 10:
Stretch về [30,120].

Bước 11:
Tính H3.

Bước 12:
Hiển thị và lưu kết quả.

---

# 13. ĐỘ PHỨC TẠP THUẬT TOÁN

Giả sử ảnh có:

[
N = H \times W
]

pixel.

Các bước chính:

* Chuyển ảnh xám: O(N)
* Histogram H1: O(N)
* Equalization: O(N)
* Histogram H2: O(N)
* Stretch: O(N)
* Histogram H3: O(N)

Tổng:

[
O(N)
]

Do đó chương trình có thể xử lý hiệu quả nhiều ảnh liên tiếp.

---

# 14. KẾT LUẬN

Chương trình thực hiện đầy đủ quy trình xử lý Histogram:

```text
RGB
↓
Gray
↓
H1
↓
Equalization
↓
H2
↓
Stretch [30,120]
↓
H3
↓
Save
```

Thuật toán giúp cải thiện độ tương phản, chuẩn hóa phân bố mức xám và hỗ trợ phân tích ảnh hiệu quả hơn.
