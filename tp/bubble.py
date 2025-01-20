import matplotlib.pyplot as plt
import numpy as np


def draw_bubble_chart():
    # 生成数据
    np.random.seed(19680801)
    N = 50
    x = np.random.rand(N)
    y = np.random.rand(N)
    colors = np.random.rand(N)
    area = (30 * np.random.rand(N)) ** 2  # 气泡的面积，使用平方来表示大小

    plt.scatter(x, y, s=area, c=colors, alpha=0.5)
    plt.colorbar()  # 显示颜色条
    plt.title('bubble') 
    plt.xlabel('X axis') 
    plt.ylabel('Y axis') 
    plt.show()


if __name__ == "__main__":
    draw_bubble_chart()