import cv2
import numpy as np
from pathlib import Path
import project_points as pp
import matplotlib.pyplot as plt
import pose_vector_to_transformation_matrix as pttm
import distort_points as dp
path=Path((Path(__file__).parent)).parent
image = cv2.imread(str(path / "data" / "images" / "img_0001.jpg"), cv2.IMREAD_COLOR)
K = pttm.calcul_K()
image_undistorted = np.zeros_like(image)
height, width = image.shape[:2]
for y in range(height):
    for x in range(width):
        u, v = dp.distort_points(x, y, K)
        u = int(round(u))
        v = int(round(v))
        if 0 <= u < width and 0 <= v < height:
            image_undistorted[y, x] = image[v, u]
cv2.imshow("image", image_undistorted)
cv2.waitKey(0)
cv2.destroyAllWindows()
