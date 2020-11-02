from cv2 import cv2
import numpy as np

img = cv2.imread("C:\\Users\\Khiem472\\Downloads\\Kanao.jpg", cv2.IMREAD_GRAYSCALE)
freq_img = np.fft.fft2(img)
freq_img = np.fft.fftshift(freq_img)

def D(p1, p2):
   return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def ButterworthFilter(size, D0, n):
   x, y = size
   mask = np.zeros(size)
   center = (x/2, y/2)
   for j in range(y):
      for i in range(x):
         mask[i,j] = 1/(1 + (D((i,j), center)/D0)**(2*n))
   return mask

mask = ButterworthFilter(img.shape, 80, 3)

filtered_freq_img = freq_img * mask
filtered_freq_img = np.fft.ifftshift(filtered_freq_img)
filtered_img = np.fft.ifft2(filtered_freq_img)

real_img = np.array(np.round(np.abs(filtered_img)), dtype=np.uint8)
cv2.imshow("hihi", real_img)
cv2.waitKey(0)
cv2.imshow("hoho", img)
cv2.waitKey(0)