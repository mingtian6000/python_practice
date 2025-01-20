import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jn
from IPython.display import display, clear_output
import time

x = np.linspace(0,5)
f, ax = plt.subplots()
ax.set_title("Bessel functions")
plt.ion()  
for n in range(1,10):
    time.sleep(1)
    ax.plot(x, jn(x,n))
    clear_output(wait=True)
    display(f)
    plt.pause(0.5)  

plt.show()  # 显示图片，防止闪退

plt.close()
