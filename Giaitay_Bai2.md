📘TÀI LIỆU GIẢI THÍCH VÀ HƯỚNG DẪN TỰ CODE – PHÉP TÍCH CHẬP VÀ MEDIAN FILTER
Mục đích: Giúp hiểu bản chất của phép tích chập (Convolution), Median Filter và cách tạo các ảnh I1, I2, I3, I4, I5, I6 theo đúng yêu cầu đề bài.

MỤC LỤC
Đề bài
Chuyển ảnh màu sang ảnh xám
Phép tích chập (Convolution)
Tạo ảnh I1 bằng Kernel 3×3
Tạo ảnh I2 bằng Kernel 5×5
Tạo ảnh I3 bằng Kernel 7×7 và Stride = 2
Median Filter
Tạo ảnh I4
Tạo ảnh I5
Đồng bộ kích thước ảnh
Tạo ảnh I6
Quy trình xử lý toàn bộ ảnh
Hướng dẫn tự code lại
Bảng tổng kết

1. ĐỀ BÀI
Cho ảnh màu I kích thước n × m.
Thực hiện:
Chuyển ảnh sang ảnh xám.
Tạo I1 bằng kernel 3×3.
Tạo I2 bằng kernel 5×5.
Tạo I3 bằng kernel 7×7.
Dùng stride = 2 cho I3.
Tạo I4 bằng Median Filter 3×3 trên I3.
Tạo I5 bằng Median Filter 5×5 trên I1.
Padding ảnh nhỏ hơn.
Tạo I6 theo:
Nếu I4(x,y) > I5(x,y)
→ I6(x,y) = 0
Ngược lại
→ I6(x,y) = I5(x,y)

2. CHUYỂN ẢNH MÀU SANG ẢNH XÁM
Tại sao phải chuyển?
Các phép lọc trong bài làm việc trên cường độ sáng của pixel.
Do đó ảnh RGB cần được chuyển sang ảnh xám.
Công thức
Gray = 0.299R + 0.587G + 0.114B
Trong code
gray = cv2.cvtColor(     img,     cv2.COLOR_BGR2GRAY )

3. PHÉP TÍCH CHẬP (CONVOLUTION)
Ý tưởng
Một kernel sẽ trượt trên toàn bộ ảnh.
Tại mỗi vị trí:
Nhân từng phần tử kernel với pixel tương ứng.
Cộng tất cả lại.
Gán cho pixel đầu ra.
Minh họa
Kernel 3×3:

Nếu vùng ảnh:

Thì:
(100+120+140 +90+110+130 +80+100+120)/9 = 110

4. TẠO ẢNH I1 – KERNEL 3×3
Kernel
kernel3 = np.ones((3,3))/9
Padding
Padding = 1
Vì:
(3 - 1)/2 = 1
Trong code
I1 = cv2.filter2D(     gray,     -1,     kernel3,     borderType=cv2.BORDER_CONSTANT )

5. TẠO ẢNH I2 – KERNEL 5×5
Kernel
kernel5 = np.ones((5,5))/25
Padding
Padding = 2
Vì:
(5 - 1)/2 = 2
Trong code
I2 = cv2.filter2D(     gray,     -1,     kernel5,     borderType=cv2.BORDER_CONSTANT )

6. TẠO ẢNH I3 – KERNEL 7×7 VÀ STRIDE = 2
Kernel
kernel7 = np.ones((7,7))/49
Padding
Padding = 3
Vì:
(7 - 1)/2 = 3
Bước 1
Lọc bằng kernel 7×7:
temp = cv2.filter2D(     gray,     -1,     kernel7,     borderType=cv2.BORDER_CONSTANT )
Bước 2
Mô phỏng stride = 2
I3 = temp[::2, ::2]
Nghĩa là:
Lấy hàng: 0,2,4,6,...  Lấy cột: 0,2,4,6,...
Kích thước ảnh giảm khoảng một nửa.

7. MEDIAN FILTER
Ý tưởng
Không lấy trung bình.
Thay vào đó:
Lấy toàn bộ giá trị trong cửa sổ.
Sắp xếp tăng dần.
Lấy phần tử ở giữa.
Ví dụ:
20 50 40 80 90 10 60 30 70
Sau khi sắp xếp:
10 20 30 40 50 60 70 80 90
Median = 50

8. TẠO I4
Median 3×3 trên I3
I4 = cv2.medianBlur(I3, 3)

9. TẠO I5
Median 5×5 trên I1
I5 = cv2.medianBlur(I1, 5)

10. ĐỒNG BỘ KÍCH THƯỚC
Vấn đề
I4 được tạo từ I3.
Do I3 dùng stride = 2 nên nhỏ hơn I5.
Không thể so sánh trực tiếp.
Giải pháp
Padding ảnh nhỏ hơn bằng 0.
pad_I4 = np.zeros((new_h,new_w)) pad_I5 = np.zeros((new_h,new_w))
Sau đó chép dữ liệu vào góc trên trái.

11. TẠO I6
Luật
Nếu:
I4(x,y) > I5(x,y)
thì:
I6(x,y) = 0
Ngược lại:
I6(x,y) = I5(x,y)
Công thức
I6(x,y) = 0       nếu I4 > I5  I5      nếu I4 ≤ I5
Trong code
I6 = np.where(     pad_I4 > pad_I5,     0,     pad_I5 )

12. QUY TRÌNH XỬ LÝ TOÀN BỘ ẢNH
Ảnh màu    │    ▼ Ảnh xám    │    ├──► I1 (Kernel 3×3)    │    ├──► I2 (Kernel 5×5)    │    └──► I3 (Kernel 7×7 + Stride=2)                 │                 ▼             I4 (Median 3×3)  I1  │  ▼ I5 (Median 5×5)  I4 + I5    │    ▼  Padding    │    ▼     I6

13. HƯỚNG DẪN TỰ CODE LẠI
Bước A
Đọc ảnh và chuyển sang ảnh xám
img = cv2.imread(path) gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
Bước B
Tạo 3 kernel
kernel3 kernel5 kernel7
Bước C
Tính I1, I2, I3
filter2D(...)
Bước D
Tính I4, I5
medianBlur(...)
Bước E
Padding
pad_I4 pad_I5
Bước F
Tạo I6
np.where(...)
Bước G
Lưu kết quả
cv2.imwrite(...)

14. BẢNG TỔNG KẾT


Mẹo kiểm tra kết quả:
I1 mịn hơn ảnh gốc.
I2 mịn hơn I1.
I3 nhỏ hơn do stride = 2.
I4 giảm nhiễu trên I3.
I5 giảm nhiễu trên I1.
I6 chỉ giữ lại các giá trị thỏa điều kiện I4 ≤ I5.
