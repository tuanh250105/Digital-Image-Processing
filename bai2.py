import cv2
import numpy as np
import matplotlib.pyplot as plt

# Đọc ảnh màu

img = cv2.imread("anhbai2.2.jpeg")

if img is None:
    print("Không đọc được ảnh!")
    exit()

# Chuyển ảnh xám

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Tạo các kernel

kernel3 = np.ones((3, 3), dtype=np.float32) / 9
kernel5 = np.ones((5, 5), dtype=np.float32) / 25
kernel7 = np.ones((7, 7), dtype=np.float32) / 49

# I1: Kernel 3x3, padding = 1

I1 = cv2.filter2D(
    gray,
    -1,
    kernel3,
    borderType=cv2.BORDER_CONSTANT
)

# I2: Kernel 5x5, padding = 2

I2 = cv2.filter2D(
    gray,
    -1,
    kernel5,
    borderType=cv2.BORDER_CONSTANT
)

# I3: Kernel 7x7, padding = 3
# stride = 2

temp = cv2.filter2D(
    gray,
    -1,
    kernel7,
    borderType=cv2.BORDER_CONSTANT
)

# Mô phỏng stride = 2
I3 = temp[::2, ::2]

# I4: Median Filter 3x3 trên I3

I4 = cv2.medianBlur(I3, 3)

# I5: Median Filter 5x5 trên I1

I5 = cv2.medianBlur(I1, 5)

# Đồng bộ kích thước bằng padding

h4, w4 = I4.shape
h5, w5 = I5.shape

new_h = max(h4, h5)
new_w = max(w4, w5)

pad_I4 = np.zeros((new_h, new_w), dtype=np.uint8)
pad_I5 = np.zeros((new_h, new_w), dtype=np.uint8)

pad_I4[:h4, :w4] = I4
pad_I5[:h5, :w5] = I5

# I6
# Nếu I4(x,y) > I5(x,y) thì I6 = 0
# Ngược lại I6 = I5

I6 = np.where(pad_I4 > pad_I5, 0, pad_I5)
I6 = I6.astype(np.uint8)

# In kích thước ảnh

print("Gray:", gray.shape)
print("I1:", I1.shape)
print("I2:", I2.shape)
print("I3:", I3.shape)
print("I4:", I4.shape)
print("I5:", I5.shape)
print("Pad I4:", pad_I4.shape)
print("Pad I5:", pad_I5.shape)
print("I6:", I6.shape)

# Hiển thị kết quả

titles = [
    "Gray",
    "I1 Kernel 3x3",
    "I2 Kernel 5x5",
    "I3 Kernel 7x7 Stride=2",
    "I4 Median 3x3",
    "I5 Median 5x5",
    "I6"
]

images = [
    gray,
    I1,
    I2,
    I3,
    pad_I4,
    pad_I5,
    I6
]

plt.figure(figsize=(15, 8))

for i in range(len(images)):
    plt.subplot(2, 4, i + 1)
    plt.imshow(images[i], cmap="gray")
    plt.title(titles[i])
    plt.axis("off")

plt.tight_layout()
plt.show()

# Lưu ảnh kết quả

cv2.imwrite("Gray.jpg", gray)
cv2.imwrite("I1.jpg", I1)
cv2.imwrite("I2.jpg", I2)
cv2.imwrite("I3.jpg", I3)
cv2.imwrite("I4.jpg", pad_I4)
cv2.imwrite("I5.jpg", pad_I5)
cv2.imwrite("I6.jpg", I6)

print("Hoàn thành!")