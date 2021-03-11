import cv2
import glob
import numpy as np

inner_corner = (6, 9)
size = 2.5 #mỗi ô vuông có kích cỡ 2.5cm x 2.5cm

real_world_points = np.zeros((54,3), np.float32)
for i in range(real_world_points.shape[0]):
   real_world_points[i][0] = i % inner_corner[0]
   real_world_points[i][1] = i // inner_corner[0]

real_world_points = size*real_world_points

path = 'Desktop\\a\\*.jpg'
world_coor_system = []
image_coor_system = []
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01)

images = glob.glob(path)
total_error1 = 0
for file in images:
   img = cv2.imread(file)
   img = cv2.resize(img, (800, 600))
   img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

   found, corners = cv2.findChessboardCorners(img, inner_corner)
   if found == True:
      world_coor_system.append(real_world_points)
      imgcorners = cv2.cornerSubPix(img, corners, (11,11), (-1,-1), criteria)
      image_coor_system.append(imgcorners)
      img = cv2.drawChessboardCorners(img, inner_corner, imgcorners, found)
      _, camera, distort, rotation, translation = cv2.calibrateCamera(world_coor_system, image_coor_system, img.shape[::-1], None, None)
      
      img = cv2.imread(file)
      result = cv2.undistort(img, camera, distort)
      out = np.hstack((img, result))
      cv2.imwrite('out.jpg', out)

      total_error2 = 0
      for i in range(len(world_coor_system)):
         points, _ = cv2.projectPoints(world_coor_system[i], rotation[i], translation[i], camera, distort)
         running_error = cv2.norm(image_coor_system[i],points, cv2.NORM_L2)/len(points)
         total_error2 += running_error
      if total_error2 < total_error1:
         np.savetxt('camera matrix.txt', camera)
         np.savetxt('distort coefficients.txt', distort)
         total_error1 = total_error2

      