# 📘 TÀI LIỆU GIẢI VÀ HƯỚNG DẪN TỰ CODE – TOÁN TỬ LBP

> **Mục đích:** Tài liệu này giúp bạn và đồng nghiệp hiểu rõ bản chất toán học của thuật toán LBP và có thể tự tay code lại từ đầu mà không cần tham khảo code mẫu.

---

## MỤC LỤC

1. [ĐỀ BÀI](#1-đề-bài)
2. [LBP LÀ GÌ?](#2-lbp-là-gì)
3. [BƯỚC 1 – CHUYỂN ẢNH SANG XÁM](#3-bước-1--chuyển-ảnh-sang-xám)
4. [BƯỚC 2 – TÍNH TỌA ĐỘ ĐIỂM LÂN CẬN](#4-bước-2--tính-tọa-độ-điểm-lân-cận)
5. [BƯỚC 3 – NỘI SUY SONG TUYẾN](#5-bước-3--nội-suy-song-tuyến)
6. [BƯỚC 4 – TẠO CHUỖI BIT](#6-bước-4--tạo-chuỗi-bit)
7. [BƯỚC 5 – CHUYỂN SANG SỐ THẬP PHÂN](#7-bước-5--chuyển-sang-số-thập-phân)
8. [BƯỚC 6 – XỬ LÝ ĐẶC BIỆT P=16 VÀ P=24](#8-bước-6--xử-lý-đặc-biệt-p16-và-p24)
9. [BƯỚC 7 – LẶP CHO TOÀN BỘ ẢNH](#9-bước-7--lặp-cho-toàn-bộ-ảnh)
10. [VÍ DỤ SỐ GIẢI TAY ĐẦY ĐỦ](#10-ví-dụ-số-giải-tay-đầy-đủ)
11. [HƯỚNG DẪN TỰ CODE LẠI](#11-hướng-dẫn-tự-code-lại)
12. [BẢNG TỔNG KẾT 5 CẤU HÌNH](#12-bảng-tổng-kết-5-cấu-hình)

---

## 1. ĐỀ BÀI

Cho 1 ảnh màu **I** kích thước $n \times m$, chuyển đổi ảnh **I** thành ảnh xám. Dùng toán tử **LBP (Local Binary Patterns)** để biến đổi ảnh **I** theo các yêu cầu sau:

- **P = 8**, R = 1 và R = 2
- **P = 16**, R = 2 và R = 3
- **P = 24**, R = 3

**Ghi chú quan trọng từ đề:** Trường hợp P = 16 (hoặc P = 24) thì tách chuỗi nhị phân thành 2 phần (hoặc 3 phần). Mỗi phần có 8 bits. Sau đó chỉ lấy phần có **giá trị lớn nhất** gán cho pixel đang xét.

---

## 2. LBP LÀ GÌ?

**LBP (Local Binary Patterns)** là phương pháp mô tả kết cấu (texture) cục bộ của ảnh.

**Ý tưởng cốt lõi rất đơn giản:**

> Với mỗi pixel trong ảnh, nhìn ra các điểm xung quanh nó trên một vòng tròn bán kính R và hỏi:
> *"Điểm lân cận này có sáng hơn hoặc bằng pixel trung tâm không?"*
> - **Có** → ghi **1**
> - **Không** → ghi **0**
>
> Ghép tất cả lại → được một chuỗi bit → chuyển sang số thập phân → gán cho pixel đó.

| Tham số | Ý nghĩa |
|:---:|:---|
| **P** | Số điểm lân cận lấy mẫu trên vòng tròn |
| **R** | Bán kính vòng tròn (đơn vị: pixel) |

---

## 3. BƯỚC 1 – CHUYỂN ẢNH SANG XÁM

### Tại sao cần chuyển?
LBP so sánh **độ sáng** → chỉ cần 1 giá trị cường độ sáng cho mỗi pixel → dùng ảnh xám.

### Công thức (ITU-R BT.601):
$$\text{Gray} = 0.299 \times R + 0.587 \times G + 0.114 \times B$$

Trọng số khác nhau vì mắt người nhạy cảm với màu xanh lá (G) nhất, kém nhạy với xanh dương (B) nhất.

### Trong code:
```python
img_pil = Image.open(duong_dan).convert('L')    # PIL tự áp công thức trên
img_xam = np.array(img_pil, dtype=np.float64)   # chuyển sang ma trận số thực
```

> **Lưu ý:** Dùng `dtype=np.float64` để phép tính nội suy sau đó không bị mất độ chính xác.

### Kết quả:
```
Ảnh màu RGB (n × m × 3)   →   Ảnh xám (n × m)
pixel [R, G, B]            →   pixel Gray ∈ [0, 255]
```

---

## 4. BƯỚC 2 – TÍNH TỌA ĐỘ ĐIỂM LÂN CẬN

### Vấn đề:
P điểm lân cận được rải **đều** trên vòng tròn bán kính R. Khi P = 8 và R = 1 thì tọa độ vừa hay là số nguyên (dễ). Khi P = 16 hoặc R = 2, 3 thì **tọa độ là số thực** → không trùng vào ô pixel nguyên nào → cần nội suy.

### Công thức tọa độ điểm lân cận thứ $p$:

$$x_p = cx + R \times \cos\!\left(\frac{2\pi \times p}{P}\right)$$

$$y_p = cy - R \times \sin\!\left(\frac{2\pi \times p}{P}\right)$$

> ⚠️ **Dấu trừ ở $y_p$:** Trong hệ tọa độ ảnh, trục Y đi từ **trên xuống dưới** (ngược với toán học thông thường). Do đó phải đổi dấu sin.

### Ví dụ P=8, R=1, pixel trung tâm (cx=4, cy=4):

| p | Góc | $x_p$ | $y_p$ | Loại tọa độ |
|:-:|:---:|:-----:|:-----:|:---:|
| 0 | 0° | 5.000 | 4.000 | ✅ Nguyên |
| 1 | 45° | 4.707 | 3.293 | ⚠️ Thực |
| 2 | 90° | 4.000 | 3.000 | ✅ Nguyên |
| 3 | 135° | 3.293 | 3.293 | ⚠️ Thực |
| 4 | 180° | 3.000 | 4.000 | ✅ Nguyên |
| 5 | 225° | 3.293 | 4.707 | ⚠️ Thực |
| 6 | 270° | 4.000 | 5.000 | ✅ Nguyên |
| 7 | 315° | 4.707 | 4.707 | ⚠️ Thực |

### Trong code:
```python
for p in range(P):
    goc = 2 * np.pi * p / P
    xp  = cx + R * np.cos(goc)
    yp  = cy - R * np.sin(goc)   # dấu trừ!
```

---

## 5. BƯỚC 3 – NỘI SUY SONG TUYẾN

### Vấn đề:
Điểm lân cận tại tọa độ thực $(x_p, y_p)$ không rơi vào đúng ô pixel nào → phải **ước lượng** giá trị độ sáng tại đó từ 4 pixel nguyên bao quanh.

### Các bước thực hiện:

**Bước 3.1 – Tìm 4 pixel góc:**
```
x0 = floor(xp)        x1 = x0 + 1
y0 = floor(yp)        y1 = y0 + 1

      col=x0     col=x1
row=y0  [f00]────[f01]
          │   ★   │
row=y1  [f10]────[f11]
```

**Bước 3.2 – Tính khoảng cách:**
$$dx = x_p - x_0 \quad (0 \leq dx < 1)$$
$$dy = y_p - y_0 \quad (0 \leq dy < 1)$$

**Bước 3.3 – Nội suy theo công thức:**
$$g_p = (1-dy)(1-dx) \cdot f_{00} + (1-dy) \cdot dx \cdot f_{01} + dy \cdot (1-dx) \cdot f_{10} + dy \cdot dx \cdot f_{11}$$

> **Cách nhớ:** Pixel nào **gần** điểm ★ hơn thì được tính **trọng số lớn hơn**. Tổng 4 trọng số luôn = 1.

### Trong code:
```python
def noi_suy_song_tuyen(anh, y, x):
    x0 = int(np.floor(x));  x1 = x0 + 1
    y0 = int(np.floor(y));  y1 = y0 + 1
    # clip để không vượt biên ảnh
    x0 = np.clip(x0, 0, cols-1);  x1 = np.clip(x1, 0, cols-1)
    y0 = np.clip(y0, 0, rows-1);  y1 = np.clip(y1, 0, rows-1)
    dx = x - np.floor(x)
    dy = y - np.floor(y)
    f00 = anh[y0, x0];  f01 = anh[y0, x1]
    f10 = anh[y1, x0];  f11 = anh[y1, x1]
    return (1-dy)*(1-dx)*f00 + (1-dy)*dx*f01 + dy*(1-dx)*f10 + dy*dx*f11
```

---

## 6. BƯỚC 4 – TẠO CHUỖI BIT

### Công thức:
$$\text{bit}_p = \begin{cases} 1 & \text{nếu } g_p \geq g_c \quad \text{(lân cận sáng hơn hoặc bằng)} \\ 0 & \text{nếu } g_p < g_c \quad \text{(lân cận tối hơn)} \end{cases}$$

Trong đó $g_c$ là giá trị pixel trung tâm, $g_p$ là giá trị nội suy của điểm lân cận thứ $p$.

### Kết quả:
Một chuỗi P bit theo thứ tự $p = 0, 1, 2, \ldots, P-1$:
$$[\text{bit}_0, \; \text{bit}_1, \; \text{bit}_2, \; \ldots, \; \text{bit}_{P-1}]$$

### Trong code:
```python
bits = []
for p in range(P):
    # ... tính gp ...
    bits.append(1 if gp >= gc else 0)
```

---

## 7. BƯỚC 5 – CHUYỂN SANG SỐ THẬP PHÂN

### Công thức (bit_0 = LSB – bit có trọng số nhỏ nhất):
$$V = \sum_{i=0}^{7} \text{bit}_i \times 2^i \in [0, 255]$$

### Ví dụ:
```
Chuỗi bit: [0, 0, 0, 0, 0, 1, 1, 1]
           p=0 p=1 p=2 p=3 p=4 p=5 p=6 p=7

V = 0×2⁰ + 0×2¹ + 0×2² + 0×2³ + 0×2⁴ + 1×2⁵ + 1×2⁶ + 1×2⁷
  = 0 + 0 + 0 + 0 + 0 + 32 + 64 + 128 = 224
```

### Trong code:
```python
val = sum(b * (2**i) for i, b in enumerate(nhom))  # bit_0 = 2^0 = LSB
```

---

## 8. BƯỚC 6 – XỬ LÝ ĐẶC BIỆT P=16 VÀ P=24

### Vấn đề:
- P = 8 → 8 bit → giá trị từ 0 đến 255 → **vừa đủ 1 byte** ✅
- P = 16 → 16 bit → giá trị từ 0 đến 65535 → **quá lớn** ❌
- P = 24 → 24 bit → giá trị từ 0 đến 16.777.215 → **quá lớn** ❌

### Giải pháp theo đề bài:
Tách chuỗi P bit thành các nhóm 8-bit, tính giá trị từng nhóm rồi **lấy giá trị lớn nhất**.

#### P = 16 (tách 2 nhóm):
```
16 bit: [b0, b1, b2, b3, b4, b5, b6, b7 | b8, b9, b10, b11, b12, b13, b14, b15]
         ├──────── Nhóm 1 (V1) ─────────┘ └─────────── Nhóm 2 (V2) ─────────────┘
```
$$V_1 = \sum_{i=0}^{7} b_i \times 2^i \qquad V_2 = \sum_{i=0}^{7} b_{i+8} \times 2^i$$
$$\text{LBP} = \max(V_1, V_2)$$

#### P = 24 (tách 3 nhóm):
$$V_1 = \sum_{i=0}^{7} b_i \times 2^i \qquad V_2 = \sum_{i=0}^{7} b_{i+8} \times 2^i \qquad V_3 = \sum_{i=0}^{7} b_{i+16} \times 2^i$$
$$\text{LBP} = \max(V_1, V_2, V_3)$$

### Trong code:
```python
so_nhom = P // 8          # P=8→1, P=16→2, P=24→3
gia_tri_nhom = []
for g in range(so_nhom):
    nhom = bits[g*8 : (g+1)*8]
    val  = sum(b * (2**i) for i, b in enumerate(nhom))
    gia_tri_nhom.append(val)
gia_tri_lbp = max(gia_tri_nhom)
```

---

## 9. BƯỚC 7 – LẶP CHO TOÀN BỘ ẢNH

### Vùng hợp lệ (tránh biên):
Với bán kính R, các pixel quá gần mép ảnh không có đủ lân cận → bỏ qua (gán 0).

$$\text{Biên bỏ qua} = \lceil R \rceil \text{ pixel ở mỗi phía}$$

### Quy trình tổng quát:
```
Với mỗi pixel (cy, cx) trong vùng hợp lệ:
│
├─ 1. gc = img_xam[cy, cx]
│
├─ 2. Với p = 0, 1, ..., P-1:
│    ├─ Tính góc = 2π × p / P
│    ├─ Tính xp = cx + R × cos(góc)
│    ├─ Tính yp = cy - R × sin(góc)
│    ├─ Tính gp = nội suy song tuyến tại (xp, yp)
│    └─ bit_p = 1 nếu gp ≥ gc, ngược lại = 0
│
├─ 3. Chia P bit thành nhóm 8-bit → tính V1, V2, V3...
│
└─ 4. img_lbp[cy, cx] = max(V1, V2, V3...)
```

### Trong code:
```python
def tinh_lbp_toan_anh(anh_xam, P, R):
    rows, cols = anh_xam.shape
    anh_lbp = np.zeros((rows, cols), dtype=np.uint8)
    bien = int(np.ceil(R))
    for cy in range(bien, rows - bien):
        for cx in range(bien, cols - bien):
            anh_lbp[cy, cx] = tinh_lbp_mot_pixel(anh_xam, cy, cx, P, R)
    return anh_lbp
```

---

## 10. VÍ DỤ SỐ GIẢI TAY ĐẦY ĐỦ

**Đề:** Tính giá trị LBP tại pixel trung tâm $(cx=5, cy=5)$ với cấu hình **P=8, R=1**.

**Ma trận ảnh xám 3×3 xung quanh vùng đang xét:**
```
          col=4    col=5    col=6
row=4:    [110]    [130]    [145]
row=5:    [ 90]    [120]    [115]     ← gc = 120
row=6:    [105]    [ 95]    [140]
```

**Bước 1: Lấy gc = img_xam[5, 5] = 120**

**Bước 2: Tính tọa độ 8 điểm lân cận (P=8, R=1):**

| p | Góc | $x_p$ | $y_p$ | $f_{00}$ | $f_{01}$ | $f_{10}$ | $f_{11}$ | dx | dy | $g_p$ | bit |
|:-:|:---:|:-----:|:-----:|:--------:|:--------:|:--------:|:--------:|:--:|:--:|:-----:|:---:|
| 0 | 0° | **6.000** | **5.000** | – | – | – | – | 0 | 0 | **115** | 0 |
| 1 | 45° | **5.707** | **4.293** | img[4,5]=130 | img[4,6]=145 | img[5,5]=120 | img[5,6]=115 | 0.707 | 0.293 | **133.9** | 1 |
| 2 | 90° | **5.000** | **4.000** | – | – | – | – | 0 | 0 | **130** | 1 |
| 3 | 135° | **4.293** | **4.293** | img[4,4]=110 | img[4,5]=130 | img[5,4]=90 | img[5,5]=120 | 0.293 | 0.293 | **118.2** | 0 |
| 4 | 180° | **4.000** | **5.000** | – | – | – | – | 0 | 0 | **90** | 0 |
| 5 | 225° | **4.293** | **5.707** | img[5,4]=90 | img[5,5]=120 | img[6,4]=105 | img[6,5]=95 | 0.293 | 0.707 | **101.8** | 0 |
| 6 | 270° | **5.000** | **6.000** | – | – | – | – | 0 | 0 | **95** | 0 |
| 7 | 315° | **5.707** | **5.707** | img[5,5]=120 | img[5,6]=115 | img[6,5]=95 | img[6,6]=140 | 0.707 | 0.707 | **117.5** | 0 |

> *Lưu ý: Các điểm có tọa độ nguyên thì lấy thẳng từ ảnh (dx=0, dy=0).*

**Ví dụ tính $g_p$ tại p=1** (tọa độ thực $x_p=5.707$, $y_p=4.293$):
$$dx = 5.707 - 5 = 0.707 \qquad dy = 4.293 - 4 = 0.293$$
$$g_1 = (1-0.293)(1-0.707) \times 130 + (1-0.293)(0.707) \times 145$$
$$\quad + 0.293(1-0.707) \times 120 + 0.293 \times 0.707 \times 115$$
$$= 0.707 \times 0.293 \times 130 + 0.707 \times 0.707 \times 145 + 0.293 \times 0.293 \times 120 + 0.293 \times 0.707 \times 115$$
$$= 26.94 + 72.48 + 10.30 + 23.85 = 133.57 \approx 133.9$$

**Bước 3: Chuỗi 8 bit:**
$$[\text{bit}_0, \text{bit}_1, \ldots, \text{bit}_7] = [0, 1, 1, 0, 0, 0, 0, 0]$$

**Bước 4: Tính V1 (P=8 → chỉ có 1 nhóm 8-bit):**
$$V_1 = 0 \times 2^0 + 1 \times 2^1 + 1 \times 2^2 + 0 \times 2^3 + 0 \times 2^4 + 0 \times 2^5 + 0 \times 2^6 + 0 \times 2^7$$
$$= 0 + 2 + 4 + 0 + 0 + 0 + 0 + 0 = \boxed{6}$$

**Kết quả:** $\text{img\_lbp}[5, 5] = \max(V_1) = 6$

---

## 11. HƯỚNG DẪN TỰ CODE LẠI

Nếu bạn muốn tự code lại từ đầu, hãy làm theo thứ tự này:

### Bước A – Viết hàm nội suy song tuyến
```python
def noi_suy_song_tuyen(anh, y, x):
    # 1. Tìm x0, y0, x1, y1
    # 2. Clip tọa độ trong biên ảnh
    # 3. Tính dx = x - floor(x), dy = y - floor(y)
    # 4. Lấy f00, f01, f10, f11 từ ảnh
    # 5. Trả về giá trị nội suy theo công thức
    pass
```

### Bước B – Viết hàm tính LBP cho 1 pixel
```python
def tinh_lbp_mot_pixel(anh_xam, cy, cx, P, R):
    # 1. Lấy gc = anh_xam[cy, cx]
    # 2. Vòng lặp p = 0..P-1:
    #    a. Tính góc = 2π×p/P
    #    b. Tính xp, yp
    #    c. Gọi noi_suy_song_tuyen lấy gp
    #    d. So sánh gp >= gc → bit
    # 3. Chia bits thành nhóm 8-bit, tính val từng nhóm
    # 4. Trả về max(val)
    pass
```

### Bước C – Viết hàm xử lý toàn ảnh
```python
def tinh_lbp_toan_anh(anh_xam, P, R):
    # 1. Tạo ma trận kết quả toàn 0, dtype=uint8
    # 2. Tính bien = ceil(R)
    # 3. Vòng lặp cy, cx trong vùng hợp lệ:
    #    anh_lbp[cy, cx] = tinh_lbp_mot_pixel(...)
    # 4. Trả về anh_lbp
    pass
```

### Bước D – Ghép tất cả lại và chạy
```python
import numpy as np
from PIL import Image

# Đọc ảnh xám
img = Image.open('anh.jpg').convert('L')
img_xam = np.array(img, dtype=np.float64)

# Áp dụng 5 cấu hình
for P, R in [(8,1), (8,2), (16,2), (16,3), (24,3)]:
    ket_qua = tinh_lbp_toan_anh(img_xam, P, R)
    # hiển thị hoặc lưu kết quả
```

---

## 12. BẢNG TỔNG KẾT 5 CẤU HÌNH

| STT | P | R | Số nhóm | Kết quả | Đặc điểm |
|:---:|:-:|:-:|:-------:|:-------:|:----------|
| 1 | 8 | 1 | 1 | $V_1$ | Vùng nhỏ nhất, cơ bản nhất, nhạy với chi tiết mịn |
| 2 | 8 | 2 | 1 | $V_1$ | Vùng rộng hơn R=1, ít nhạy nhiễu hơn |
| 3 | 16 | 2 | 2 | $\max(V_1, V_2)$ | Nhiều hướng hơn (22.5°/hướng), mô tả chi tiết hơn |
| 4 | 16 | 3 | 2 | $\max(V_1, V_2)$ | Nhiều hướng + vùng rộng |
| 5 | 24 | 3 | 3 | $\max(V_1, V_2, V_3)$ | Chi tiết nhất (15°/hướng), vùng rộng nhất |

---

> [!TIP]
> **Mẹo kiểm tra kết quả đúng hay sai:** Chọn 1 pixel bất kỳ trong ảnh, tự tính tay theo từng bước ở Mục 10, sau đó so sánh với giá trị `img_lbp[cy, cx]` mà code trả về. Nếu trùng nhau → code đúng!

> [!NOTE]
> **Tại sao dùng vòng lặp `for` thay vì NumPy vector hóa?** Vòng lặp `for` phản ánh đúng bản chất từng bước của thuật toán, giúp dễ hiểu, dễ debug và dễ đối chiếu giải tay. Trong nghiên cứu học thuật, tính đúng đắn quan trọng hơn tốc độ.
