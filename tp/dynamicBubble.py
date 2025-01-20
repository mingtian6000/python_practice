import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

## not work, this is not dynamic bublles..
def update(frame):
    x = np.random.normal(loc=frame, scale=1, size=100)
    y = np.random.normal(loc=frame, scale=1, size=100)
    sizes = np.random.rand(100) * 100
    colors = np.random.rand(100)
    frame.set_offsets(np.c_[x, y])
    frame.set_sizes(sizes)
    frame.set_array(colors)
    return frame


def draw_dynamic_bubble_chart():
    np.random.seed(19680801)
    x = np.random.normal(0, 1, 100)
    y = np.random.normal(0, 1, 100)
    sizes = np.random.rand(100) * 100
    colors = np.random.rand(100)

    fig, ax = plt.subplots()
    ax.scatter(x, y, c=colors, s=sizes, alpha=0.5)

    FuncAnimation(fig, update, frames=np.arange(0, 20), interval=200)
    plt.title('dynamic bubbles')
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.show()


if __name__ == "__main__":
    draw_dynamic_bubble_chart()