import numpy as np
from pathlib import Path
def distort_points(u, v, K):
    path=Path((Path(__file__).parent)).parent
    file_dist_coef=open(str (path / "data" / "D.txt"), "r").readlines()
    dist_coef = [float(x) for x in file_dist_coef[0].split()]
    u0 = K[0, 2]
    v0 = K[1, 2]
    U = u - u0
    V = v - v0
    try:
        R = []
        for i in range(len(U)):
            r = np.sqrt(U[i]**2 + V[i]**2)
            R.append(r)
    except TypeError:
        R = np.sqrt(U**2 + V**2)
   
    Ud, Vd = (1+dist_coef[0]*np.array(R)**2 + dist_coef[1]*np.array(R)**4 ) * np.array(U)+u0, (1+dist_coef[0]*np.array(R)**2 + dist_coef[1]*np.array(R)**4 ) * np.array(V)+v0
    return Ud, Vd