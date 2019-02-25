import numpy as np
from scipy.spatial import ConvexHull


a = np.array([
    [5.83e-15,  9.34e-02],
    [2.32e-16, - 1.64e-18],
    [1.59e-30, - 7.92e-13],
    [-9.39e-23,  3.51e-19],
    [5.83e-15,  9.34e-02],
    [2.32e-16, - 1.64e-18],
    [1.59e-30, - 7.92e-13],
    [-9.39e-23,  3.51e-19],
    [5.83e-15,  9.34e-02],
    [2.32e-16, - 1.64e-18],
    [1.59e-30, - 7.92e-13],
    [-9.39e-23,  3.51e-19],
    [5.83e-15,  9.34e-02],
    [2.32e-16 ,- 1.64e-18],
    [1.59e-30, - 7.92e-13],
    [-9.39e-23,  3.51e-19],
    [5.83e-15,  9.34e-02],
    [2.32e-16 ,- 1.64e-18],
    [1.59e-30 ,- 7.92e-13],
    [-9.39e-23,  3.51e-19],
    [5.83e-15,  9.34e-02],
    [2.32e-16, - 1.64e-18],
    [1.59e-30, - 7.92e-13],
    [-9.39e-23,  3.51e-19],
    [5.83e-15,  9.34e-02],
    [2.32e-16 ,- 1.64e-18],
    [1.59e-30 ,- 7.92e-13],
    [-9.39e-23,  3.51e-19],
    [5.83e-15 , 9.34e-02],
    [2.32e-16, - 1.64e-18],
    [1.59e-30 ,- 7.92e-13],
    [-9.39e-23,  3.51e-19],
    [5.83e-15 , 9.34e-02],
    [2.32e-16 ,- 1.64e-18],
    [1.59e-30 ,- 7.92e-13],
    [-9.39e-23,  3.51e-19],
    [5.83e-15 , 9.34e-02],
    [2.32e-16 ,- 1.64e-18],
    [1.59e-30 ,- 7.92e-13],
    [-9.39e-23,  3.51e-19],
    [5.83e-15 , 9.34e-02],
    [2.32e-16 ,- 1.64e-18],
    [1.59e-30 ,- 7.92e-13]]
)

# hull = ConvexHull((np.unique(a,axis=0)))
hull = ConvexHull(a)