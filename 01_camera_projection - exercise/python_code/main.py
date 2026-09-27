import cv2
import numpy as np
from pathlib import Path
import project_points as pp
import matplotlib.pyplot as plt
import pose_vector_to_transformation_matrix as pttm
import distort_points as dp
path=Path((Path(__file__).parent)).parent
image = cv2.imread(str(path / "data" / "images_undistorted" / "img_0001.jpg"), cv2.IMREAD_COLOR)

K = pttm.calcul_K()
R = pttm.cacul_R(0)
t = pttm.calcul_t(0)
points = []
for i in range (0,9):
    for j in range (0,6):
        points.append( [i*0.04, j*0.04, 0] )
points=np.array(points)
u, v = pp.project_points(points, K, R, t).T
for x, y in zip(u, v):
    cv2.circle(image, (int(x), int(y)), radius=4, color=(0, 0, 255), thickness=-1)
cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
path=Path((Path(__file__).parent)).parent
image = cv2.imread(str(path / "data" / "images_undistorted" / "img_0001.jpg"), cv2.IMREAD_COLOR)

K = pttm.calcul_K()
R = pttm.cacul_R(0)
t = pttm.calcul_t(0)
points = []
for i in range (2):
    for j in range (2):
        for k in range (2):
            points.append( [i*0.08, j*0.08, -k*0.08] )
points=np.array(points)
u, v = pp.project_points(points, K, R, t).T
n=len(points)
for i in range(n):
    for j in range(i+1, n):
        if (np.linalg.norm(points[i]-points[j])==0.08):
            point1 = (int(round(u[i])), int(round(v[i])))
            point2 = (int(round(u[j])), int(round(v[j])))
            cv2.line(image, point1, point2, color=(0, 0, 255), thickness=2)
cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
path=Path((Path(__file__).parent)).parent
image = cv2.imread(str(path / "data" / "images" / "img_0001.jpg"), cv2.IMREAD_COLOR)
K = pttm.calcul_K()
R = pttm.cacul_R(0)
t = pttm.calcul_t(0)
points = []
for i in range (0,9):
    for j in range (0,6):
        points.append( [i*0.04, j*0.04, 0] )
points=np.array(points)
u, v = pp.project_points(points, K, R, t).T
Ud, Vd =dp.distort_points(u, v, K)
for x, y in zip(Ud, Vd):
    cv2.circle(image, (int(x), int(y)), radius=4, color=(0, 0, 255), thickness=-1)
cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
