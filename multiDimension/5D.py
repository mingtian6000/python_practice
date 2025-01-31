import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation


np.random.seed(42)
n = 100
data_5d = np.random.rand(n, 5)

data_3d = data_5d[:, :3]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

sc = ax.scatter(data_3d[:, 0], data_3d[:, 1], data_3d[:, 2])

def update(frame):
    ax.view_init(elev=10, azim=frame)
    return sc,

ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=50)

plt.title('Animation of 5D Data Projection in 3D Space')

plt.show()