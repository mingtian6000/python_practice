import plotly.express as px
import pandas as pd
import numpy as np

np.random.seed(42)
x = np.random.rand(50)
y = np.random.rand(50)
z = np.random.rand(50)
category = np.random.randint(0, 3, 50) 


data = pd.DataFrame({'X': x, 'Y': y, 'Z': z, 'Category': category})

fig = px.scatter_3d(data, x='X', y='Y', z='Z', color='Category')

fig.show()