# 📘 HƯỚNG DẪN GIẢI TAY LBP & GIẢI THÍCH LUỒNG HOẠT ĐỘNG CỦA CODE

Tài liệu này được biên soạn nhằm giúp bạn và đồng nghiệp dễ dàng hiểu được bản chất toán học của thuật toán LBP (để phục vụ việc tính toán thủ công/giải tay) cũng như cách thức mã nguồn Python triển khai thuật toán này trong cả hai phiên bản: tuần tự (vòng lặp) và song song (vector hóa).

---

## MỤC LỤC
1. [HƯỚNG DẪN CÁC BƯỚC GIẢI TAY LBP](#1-hướng-dẫn-các-bước-giải-tay-lbp)
2. [VÍ DỤ SỐ MINH HỌA GIẢI TAY CHI TIẾT](#2-ví-dụ-số-minh-họa-giải-tay-chi-tiết)
3. [LUỒNG HOẠT ĐỘNG CỦA MÃ NGUỒN (WORKFLOW)](#3-luồng-hoạt-động-của-mã-nguồn-workflow)
4. [SO SÁNH CHI TIẾT MÃ NGUỒN: VÒNG LẶP VÀ VECTOR HÓA](#4-so-sánh-chi-tiết-mã-nguồn-vòng-lặp-và-vector-hóa)

---

## 1. HƯỚNG DẪN CÁC BƯỚC GIẢI TAY LBP

Để giải tay giá trị LBP cho một pixel trung tâm $C(cx, cy)$ bất kỳ với tham số $P$ (số điểm lân cận) và $R$ (bán kính), ta thực hiện lần lượt 5 bước sau:

### Bước 1: Tính tọa độ thực của các điểm lân cận thứ $p$
Với $p = 0, 1, ..., P-1$, góc tương ứng là $\theta_p = \frac{2\pi \cdot p}{P}$ (hoặc $\frac{360^\circ \cdot p}{P}$):
* $x_p = cx + R \cdot \cos(\theta_p)$
* $y_p = cy - R \cdot \sin(\theta_p)$ *(Lưu ý: dấu trừ vì trục Y của ảnh đi từ trên xuống dưới)*

### Bước 2: Nội suy song tuyến (Bilinear Interpolation) để tính giá trị sáng $g_p$
Nếu tọa độ thực $(x_p, y_p)$ là số nguyên, ta lấy trực tiếp giá trị pixel tại đó.  
Nếu $(x_p, y_p)$ là số thập phân, ta xác định 4 pixel nguyên bao quanh:
* Tọa độ góc trái-trên: $x_0 = \lfloor x_p \rfloor, \; y_0 = \lfloor y_p \rfloor \rightarrow$ Giá trị: $f_{00}$
* Tọa độ góc phải-trên: $x_1 = x_0 + 1, \; y_0 \rightarrow$ Giá trị: $f_{01}$
* Tọa độ góc trái-dưới: $x_0, \; y_1 = y_0 + 1 \rightarrow$ Giá trị: $f_{10}$
* Tọa độ góc phải-dưới: $x_1, \; y_1 \rightarrow$ Giá trị: $f_{11}$

Tính phần lẻ (khoảng cách): $dx = x_p - x_0, \quad dy = y_p - y_0$.  
Công thức tính giá trị nội suy $g_p$:
$$g_p = (1-dy)(1-dx) \cdot f_{00} + (1-dy)dx \cdot f_{01} + dy(1-dx) \cdot f_{10} + dydx \cdot f_{11}$$

### Bước 3: Tạo chuỗi bit nhị phân
So sánh giá trị lân cận $g_p$ với giá trị pixel trung tâm $g_c$:
$$\text{bit}_p = \begin{cases} 1 & \text{nếu } g_p \geq g_c \\ 0 & \text{nếu } g_p < g_c \end{cases}$$
Ta thu được chuỗi $P$ bits theo thứ tự: $[\text{bit}_0, \text{bit}_1, ..., \text{bit}_{P-1}]$.

### Bước 4: Tách nhóm 8-bit và quy đổi sang số thập phân
* Nếu **P=8**: Ta có 1 nhóm duy nhất. Giá trị LBP:
  $$V_1 = \sum_{i=0}^{7} \text{bit}_i \times 2^i$$
* Nếu **P=16**: Tách thành 2 nhóm 8-bit:
  * Nhóm 1: $[\text{bit}_0 \dots \text{bit}_7] \rightarrow V_1 = \sum_{i=0}^{7} \text{bit}_i \times 2^i$
  * Nhóm 2: $[\text{bit}_8 \dots \text{bit}_{15}] \rightarrow V_2 = \sum_{i=0}^{7} \text{bit}_{i+8} \times 2^i$
* Nếu **P=24**: Tách thành 3 nhóm 8-bit tương tự để được $V_1, V_2, V_3$.

*(Lưu ý: $\text{bit}_0, \text{bit}_8, \text{bit}_{16}$ luôn là LSB - bit có trọng số nhỏ nhất $2^0$ trong nhóm của chúng).*

### Bước 5: Lấy giá trị lớn nhất (MAX)
Gán giá trị LBP cho pixel trung tâm:
$$\text{LBP}(cx, cy) = \max(V_1, V_2, \dots)$$

---

## 2. VÍ DỤ SỐ MINH HỌA GIẢI TAY CHI TIẾT

Giả sử ta cần tính LBP tại pixel trung tâm có tọa độ **(cx=4, cy=4)** với cấu hình **P=8, R=1**.  
Giá trị pixel trung tâm: **$g_c = 120$**.

Ma trận ảnh xám $3\times3$ xung quanh điểm này như sau:
```
         col=3     col=4     col=5
row=3: [f=110]   [f=100]   [f=130]
row=4: [f=140]   [ C=120]  [f=125]
row=5: [f=105]   [f=90]    [f=150]
```

### Ví dụ tính cho hướng $p=1$ (góc $45^\circ$):
1. **Tính tọa độ lân cận thứ 1:**
   $$\theta_1 = 45^\circ = \frac{\pi}{4}$$
   $$x_1 = 4 + 1 \cdot \cos(45^\circ) = 4 + 0.707 = 4.707$$
   $$y_1 = 4 - 1 \cdot \sin(45^\circ) = 4 - 0.707 = 3.293$$

2. **Nội suy song tuyến cho điểm (4.707, 3.293):**
   * Bốn điểm góc xung quanh:
     * $x_0 = \lfloor 4.707 \rfloor = 4, \quad y_0 = \lfloor 3.293 \rfloor = 3$
     * Trái-trên: $f_{00} = \text{ảnh}[3, 4] = 100$
     * Phải-trên: $f_{01} = \text{ảnh}[3, 5] = 130$
     * Trái-dưới: $f_{10} = \text{ảnh}[4, 4] = 120$
     * Phải-dưới: $f_{11} = \text{ảnh}[4, 5] = 125$
   * Phần lẻ:
     * $dx = 4.707 - 4 = 0.707$
     * $dy = 3.293 - 3 = 0.293$
   * Áp dụng công thức nội suy:
     $$g_1 = (1-0.293)(1-0.707) \cdot 100 + (1-0.293)(0.707) \cdot 130 + 0.293(1-0.707) \cdot 120 + 0.293(0.707) \cdot 125$$
     $$g_1 = 0.707 \cdot 0.293 \cdot 100 + 0.707 \cdot 0.707 \cdot 130 + 0.293 \cdot 0.293 \cdot 120 + 0.293 \cdot 0.707 \cdot 125$$
     $$g_1 = 20.72 + 64.98 + 10.30 + 25.90 = \mathbf{121.90}$$

3. **So sánh tạo bit:**
   Vì $g_1 = 121.90 \geq g_c = 120 \rightarrow \mathbf{\text{bit}_1 = 1}$.

---

## 3. LUỒNG HOẠT ĐỘNG CỦA MÃ NGUỒN (WORKFLOW)

Dưới đây là sơ đồ luồng hoạt động tổng quát khi chương trình chạy hàng loạt nhiều ảnh trong Jupyter Notebook `LBP_chay_hang_loat.ipynb`:

```mermaid
graph TD
    A([Bắt đầu chương trình]) --> B[Đọc danh sách ảnh trong thư mục anh_xlas]
    B --> C{Còn ảnh cần xử lý?}
    C -- Hết ảnh --> Z([Kết thúc chương trình])
    C -- Còn ảnh --> D[Đọc ảnh hiện tại & Chuyển đổi sang ảnh xám bằng công thức ITU-R BT.601]
    D --> E[Lặp qua 5 cấu hình LBP]
    E --> F[Tính toán LBP toàn ảnh sử dụng Vector hóa bằng NumPy]
    F --> G[Lưu kết quả ảnh LBP vào thư mục ket_qua_lbp]
    G --> H[Vẽ & Lưu đồ thị histogram phân bố giá trị LBP]
    H --> I[In thông báo hoàn thành của ảnh hiện tại ra màn hình]
    I --> C
```

---

## 4. SO SÁNH CHI TIẾT MÃ NGUỒN: VÒNG LẶP VÀ VECTOR HÓA

Phần này cung cấp mã nguồn đầy đủ của hai giải pháp và phân tích sự tương ứng dòng lệnh để bạn và đồng nghiệp dễ dàng đối chiếu.

### 4.1. Bản đầy đủ của Mã nguồn Vòng lặp (Loop-based)
```python
def noi_suy_song_tuyen(anh, y, x):
    rows, cols = anh.shape
    x0, y0 = int(np.floor(x)), int(np.floor(y))
    x1, y1 = x0 + 1, y0 + 1
    x0 = np.clip(x0, 0, cols-1);  x1 = np.clip(x1, 0, cols-1)
    y0 = np.clip(y0, 0, rows-1);  y1 = np.clip(y1, 0, rows-1)
    dx = x - np.floor(x)
    dy = y - np.floor(y)
    f00 = anh[y0, x0]
    f01 = anh[y0, x1]
    f10 = anh[y1, x0]
    f11 = anh[y1, x1]
    return (1-dy)*(1-dx)*f00 + (1-dy)*dx*f01 + dy*(1-dx)*f10 + dy*dx*f11

def tinh_lbp_mot_pixel(anh, cy, cx, P, R):
    gc = anh[cy, cx]
    bits = []
    for p in range(P):
        goc = 2 * np.pi * p / P
        xp  = cx + R * np.cos(goc)
        yp  = cy - R * np.sin(goc)
        gp  = noi_suy_song_tuyen(anh, yp, xp)
        bits.append(1 if gp >= gc else 0)
    so_nhom = P // 8
    gia_tri_nhom = []
    for g in range(so_nhom):
        nhom = bits[g*8 : (g+1)*8]
        val  = sum(b * (2**i) for i, b in enumerate(nhom))
        gia_tri_nhom.append(val)
    return max(gia_tri_nhom)

def tinh_lbp_toan_anh_vong_lap(anh_xam, P, R):
    rows, cols = anh_xam.shape
    anh_lbp = np.zeros((rows, cols), dtype=np.uint8)
    bien = int(np.ceil(R))
    # Sử dụng 2 vòng lặp lồng nhau duyệt qua từng pixel của ảnh
    for cy in range(bien, rows - bien):
        for cx in range(bien, cols - bien):
            anh_lbp[cy, cx] = tinh_lbp_mot_pixel(anh_xam, cy, cx, P, R)
    return anh_lbp
```

### 4.2. Bản đầy đủ của Mã nguồn Vector hóa (Vectorized)
```python
def noi_suy_song_tuyen_vectorized(anh, y_coords, x_coords):
    rows, cols = anh.shape
    x0 = np.floor(x_coords).astype(np.int32)
    y0 = np.floor(y_coords).astype(np.int32)
    x1 = x0 + 1
    y1 = y0 + 1
    x0 = np.clip(x0, 0, cols - 1)
    x1 = np.clip(x1, 0, cols - 1)
    y0 = np.clip(y0, 0, rows - 1)
    y1 = np.clip(y1, 0, rows - 1)
    dx = x_coords - x0
    dy = y_coords - y0
    f00 = anh[y0, x0]
    f01 = anh[y0, x1]
    f10 = anh[y1, x0]
    f11 = anh[y1, x1]
    return (1 - dy) * (1 - dx) * f00 + (1 - dy) * dx * f01 + dy * (1 - dx) * f10 + dy * dx * f11

def tinh_lbp_vectorized(anh_xam, P, R):
    rows, cols = anh_xam.shape
    anh_lbp = np.zeros((rows, cols), dtype=np.uint8)
    bien = int(np.ceil(R))
    # Tạo lưới tọa độ cho tất cả pixel hợp lệ cùng lúc (Không dùng vòng lặp pixel)
    r_idx, c_idx = np.meshgrid(
        np.arange(bien, rows - bien),
        np.arange(bien, cols - bien),
        indexing='ij'
    )
    gc = anh_xam[r_idx, c_idx]
    bits = []
    # Chỉ lặp qua P lân cận
    for p in range(P):
        goc = 2 * np.pi * p / P
        xp = c_idx + R * np.cos(goc)
        yp = r_idx - R * np.sin(goc)
        gp = noi_suy_song_tuyen_vectorized(anh_xam, yp, xp)
        bit_p = (gp >= gc).astype(np.uint8)
        bits.append(bit_p)
    # Tách nhóm và lấy MAX trên ma trận
    so_nhom = P // 8
    ma_tran_nhom = []
    for g in range(so_nhom):
        nhom_bits = bits[g * 8 : (g + 1) * 8]
        val = np.zeros_like(r_idx, dtype=np.uint32)
        for i, b in enumerate(nhom_bits):
            val += b.astype(np.uint32) * (2 ** i)
        ma_tran_nhom.append(val)
    if so_nhom == 1:
        res = ma_tran_nhom[0]
    else:
        res = np.maximum.reduce(ma_tran_nhom)
    anh_lbp[r_idx, c_idx] = res.astype(np.uint8)
    return anh_lbp
```

---

### 4.3. Bảng ánh xạ so sánh chi tiết cơ chế hoạt động

| Bước xử lý thuật toán | Cơ chế trong Code Vòng lặp | Cơ chế tương ứng trong Code Vector hóa | Giải thích sự tương đương |
|:---|:---|:---|:---|
| **1. Xác định vùng pixel** | Lồng 2 vòng lặp duyệt qua tọa độ đơn lẻ `cy` và `cx`. | Dùng `np.meshgrid` để tạo lưới ma trận tọa độ `r_idx` và `c_idx`. | Lưới ma trận chứa tọa độ của toàn bộ $2.07$ triệu điểm ảnh. Khi tính toán ma trận, NumPy sẽ xử lý đồng thời tất cả các tọa độ này. |
| **2. Tọa độ điểm lân cận** | Tính `xp` và `yp` dạng số thực đơn lẻ cho góc $\theta_p$. | Tính `xp` và `yp` dạng mảng 2D cho góc $\theta_p$. | Thay vì lấy tọa độ lân cận cho 1 điểm, ta tạo ra bản đồ tọa độ lân cận cho toàn bộ điểm ảnh trên lưới. |
| **3. Lấy 4 điểm nguyên** | Lấy chỉ mục mảng đơn lẻ: `x0 = int(np.floor(x))`. | Lấy chỉ mục mảng dạng mảng: `x0 = np.floor(x_coords).astype(np.int32)`. | Trích xuất các ma trận chỉ mục nguyên tương ứng với các góc trái-trên, phải-trên... của toàn bộ pixel. |
| **4. Lấy độ sáng góc** | Truy cập 4 pixel đơn lẻ: `f00 = anh[y0, x0]`. | Sử dụng Advanced Indexing: `f00 = anh[y0, x0]` trên ma trận. | `f00` trong bản vector hóa là một ma trận 2D chứa độ sáng của góc trái-trên của tất cả các pixel cùng lúc. |
| **5. So sánh điều kiện** | Sử dụng biểu thức logic: `1 if gp >= gc else 0`. | Sử dụng phép so sánh ma trận logic: `(gp >= gc).astype(np.uint8)`. | Kết quả trả về là một ma trận nhị phân 2D gồm các số `0` và `1` (thay vì chỉ trả về một số nhị phân đơn lẻ). |
| **6. Chuyển thập phân** | Dùng hàm `sum()` của Python để tính tổng giá trị từng bit nhân $2^i$. | Thực hiện nhân ma trận bit với lũy thừa cơ số 2: `val += b * (2 ** i)`. | Quy đổi toàn bộ mảng bit nhị phân thành ma trận giá trị thập phân tương ứng. |
| **7. Lấy MAX nhóm** | Dùng hàm `max(V1, V2...)` trên danh sách. | Dùng hàm `np.maximum.reduce([V1, V2...])` trên ma trận. | So sánh phần tử với phần tử (element-wise) giữa các ma trận nhóm để giữ lại giá trị LBP lớn nhất cho mỗi pixel. |
