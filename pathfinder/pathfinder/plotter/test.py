import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import random

fig = plt.figure(figsize=plt.figaspect(0.5))
ax = fig.add_subplot(1, 2, 1, projection='3d')
# note this: you can skip rows!
X = [item for sublist in [[y for x in range(30)] for y in range(30)] for item in sublist]
Y = [item for sublist in [[x for x in range(30)] for y in range(30)] for item in sublist]
Z = [random.randrange(10) for x in range(30*30)]

xi = np.linspace(min(X), max(X), 100)
yi = np.linspace(min(Y), max(Y), 100)
# VERY IMPORTANT, to tell matplotlib how is your data organized
zi = griddata((X, Y), Z, (xi[None,:], yi[:,None]), method='cubic')

CS = plt.contour(xi,yi,zi,15,linewidths=0.5,color='k')
ax = fig.add_subplot(1, 2, 2, projection='3d')

xig, yig = np.meshgrid(xi, yi)

surf = ax.plot_surface(xig, yig, zi,
        linewidth=0)

plt.show()
