import numpy as np
def cacul_R(i):
    file = open("../data/poses.txt", "r")
    line = file.readlines()
    R = line[i].split()[0:9]
    W = np.array(R[0:3], dtype=float)
    Wbar=[[0, -W[2], W[1]], [W[2], 0, -W[0]], [-W[1], W[0], 0]]
    Wbar = np.array(Wbar, dtype=float)
    teta=np.linalg.norm(W)
    R = np.eye(3) + (np.sin(teta)/teta)*Wbar + ((1-np.cos(teta))/(teta**2))*(Wbar@Wbar)
    return R
def calcul_t(i):
    file = open("../data/poses.txt", "r")
    line = file.readlines()
    t = line[i].split()[3:6]
    t = np.array(t, dtype=float)
    return t
def calcul_K():
    file = open("../data/K.txt", "r")
    lines = file.readlines()
    K = []
    for line in lines:
        K.extend(line.split())
    K = np.array(K, dtype=float).reshape(3, 3)
    return K

