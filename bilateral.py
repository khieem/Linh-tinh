import numpy as np
import cv2
import sys
from math import sin, cos, exp, sqrt


def fast_Gaussian(img, sigma):
   #TODO hàm này chưa cài đặt xong
   '''
   [19] Recursively implementating the Gaussian and its derivatives
   https://hal.inria.fr/inria-00074778/document
   '''

   a0 = 1.68
   a1 = 3.735
   b0 = 1.512
   w0 = 0.6318
   c0 = -0.6803
   c1 = 0.2598
   b1 = 1.723
   w1 = 1.997

   n33 = exp(-b1/sigma-2*b0/sigma)*(c1*sin(w1/sigma)-c0*cos(w1/sigma)) + exp(-b0/sigma-2*b1/sigma)*(a1*sin(w0/sigma)-a0*cos(w0/sigma))
   n22 = 2*exp(-b0/sigma-b1/sigma) * ((a0+c0)*cos(w1/sigma)*cos(w0/sigma) - cos(w1/sigma)*a1*sin(w0/sigma) - cos(w0/sigma)*c1*sin(w1/sigma)) + c0*exp(-2*b0/sigma) + a0*exp(-2*b1/sigma)
   n11 = exp(-b1/sigma)*(c1*sin(w1/sigma)-(c0+2*a0)*cos(w1/sigma)) + exp(-b0/sigma)*(a1*sin(w0/sigma)-(2*c0+a0)*cos(w0/sigma))
   n00 = a0 + c0

   d44 = exp(-2*b0/sigma - 2*b1/sigma)
   d33 = -2*cos(w0/sigma)*exp(-b0/sigma-2*b1/sigma) - 2*cos(w1/sigma)*exp(-b1/sigma-2*b0/sigma)
   d22 = 4*cos(w1/sigma)*cos(w0/sigma)*exp(-b0/sigma-2*b1/sigma) - 2*cos(w1/sigma)*exp(-b1/sigma-2*b0/sigma)
   d11 = -2*exp(-b1/sigma)*cos(w1/sigma) - 2*exp(-b0/sigma)*cos(w0/sigma)

   def evaluate(s: str, n, a0, a1,b0,w0,c0,c1,b1,w1,n33,n22,n11,n00,d44,d33,d22,d11):
      if s[0] == 'd':
         if s[1] == 1: return d11
         if s[1] == 2: return d22
         if s[1] == 3: return d33
         if s[1] == 4: return d44
      else:
         if s[1] == 1: return n11 - d11*n00
         if s[1] == 2: return n22 - d22*n00
         if s[1] == 3: return n33 - d33*n00
         if s[1] == 4: return -d44*n00

   x, y = img.shape
   for j in range(y):
      img[j] = n00*img[j]
   


def power_iteration(A, n=1):
   '''
   tính qi - dominant eigenvector
   '''
   b = np.random.rand(A.shape[1])
   for _ in range(n):
      b1 = np.dot(A, b)
      b1_norm = np.linalg.norm(b1)
      b = b1 / b1_norm      
   return b

def Gaussian(radius, sigma):
   return np.exp(-radius/(2*sigma**2))


def bilateral_1channel(img, sigma_s, sigma_r, wsize):
   weight_sum = np.zeros(img.shape)
   result  = np.zeros(img.shape)

   for x in range(-wsize, wsize+1):
      for y in range(-wsize, wsize+1):
         spatial_weight = Gaussian(x**2+y**2, sigma_s)
         off = np.roll(img, [y, x], axis=[0,1])
         range_weight = Gaussian((off-img)**2, sigma_r)
         total_weight = spatial_weight * range_weight

         result += off*total_weight
         weight_sum += total_weight

   return result/weight_sum

def bilateral_filter(img, sigma_s, sigma_r, wsize):
   return np.stack([ 
        bilateral_1channel( img[:,:,0], sigma_s, sigma_r, wsize),   
        bilateral_1channel( img[:,:,1], sigma_s, sigma_r, wsize),
        bilateral_1channel( img[:,:,2], sigma_s, sigma_r, wsize)], axis=2)



# img = cv2.imread('/home/khikun/Desktop/Fast-Adaptive-Bilateral-Filtering-master/fish.jpg', cv2.IMREAD_UNCHANGED).astype(np.float32)/255.0

def euclid_length(vector):
   s = 0
   for i in vector:
      s += i**2   
   return sqrt(s)


def w(j, rho):
   return exp(-euclid_length(j)/(2*rho**2))
   
def f_hat(img, rho):
   '''
   f_hat là average local intensity
   hàm này cài đặt dựa trên (12)
   '''
   rs = 0
   for x in range(-rho, rho+1):
      for y in range(-rho, rho+1):
         shift = np.roll(img, [y,x], axis=[0,1])
         rs += w([x,y], rho) * shift
   return rs

def C(img, rho):
   #TODO hàm này chưa cài đặt được
   '''
   tính local covariance, cài đặt dựa trên (13)
   '''
   rs = 0
   for x in range(-rho, rho+1):
      for y in range(-rho, rho+1):
         shift = np.roll(img, [y,x], axis=[0,1])
         offset = shift - img
         k = np.tensordot(offset, np.transpose(offset, (1,0,2)), axes=([1,0], [0,1]))
         rs += w([x,y], rho) * k
   return rs


img = cv2.imread('/home/khikun/Desktop/fish.jpg', cv2.IMREAD_UNCHANGED).astype(np.float32)/255.0
filtered_img = bilateral_filter(img, 10.0, 0.1, 30)


# img = cv2.imread('/home/khikun/Desktop/house.jpg', cv2.IMREAD_UNCHANGED).astype(np.float32)/255.0
# filtered_img = bilateral_1channel(img, 10.0, 0.1, 30)

out = np.hstack([img, filtered_img])
cv2.imshow('hihihoho', out)
cv2.waitKey(0)
