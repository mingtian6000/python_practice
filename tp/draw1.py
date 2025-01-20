import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

def matplotlib_scatter():
    x = np.random.rand(50)
    y = np.random.rand(50)
    plt.scatter(x, y)
    plt.title('matplotlib scatter')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.savefig("matplotlib_scatter.png")
    plt.show()

def seaborn_scatter():
    x = np.random.rand(50)
    y = np.random.rand(50)
    data = pd.DataFrame({'x': x, 'y': y})
    sns.scatterplot(data=data, x='x', y='y')
    plt.title('seaborn scatter')
    plt.savefig("seaborn_scatter.png")
    plt.show()
    
    
if __name__ == "__main__":
    matplotlib_scatter()
    seaborn_scatter()