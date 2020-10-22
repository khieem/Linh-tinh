from PIL import Image
import numpy as np

img = Image.open('/home/khikun/Downloads/cho-ta-ava-001.jpg')
im_array = np.array(img)
im_array = np.transpose(im_array, (2,0,1))

mask = [None]*8
mask[0] = np.array([[5,-3,-3],[5,0,-3],[5,-3,-3]])
mask[1] = np.array([[5,5,-3],[5,0,-3],[-3,-3,-3]])
mask[2] = np.array([[5,5,5],[-3,0,-3],[-3,-3,-3]])
mask[3] = np.array([[-3,5,5],[-3,0,5],[-3,-3,-3]])
mask[4] = np.array([[-3,-3,5],[-3,0,5],[-3,-3,5]])
mask[5] = np.array([[-3,-3,-3],[-3,0,5],[-3,5,5]])
mask[6] = np.array([[-3,-3,-3],[-3,0,-3],[5,5,5]])
mask[7] = np.array([[-3,-3,-3],[5,0,-3],[5,5,-3]])

def convolution(image, mask):
   y, x = image.shape
   
   pad_image = np.zeros((y+2, x+2))
   pad_image[1:1+y,1:1+x] = image
   
   out = np.zeros((y, x))
   for i in range(y):
      for j in range(x):
         out[i][j] = np.sum(pad_image[i:i+3, j:j+3] * mask)

   return out

y, x = img.size
output = np.zeros((8, x, y))

for i in range(8):
   output[i] = convolution(im_array[0], mask[i])
output = np.max(output, 0)

edge_img = Image.fromarray(output)
img.show()
edge_img.show()
