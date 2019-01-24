import numpy as np
import matplotlib.pyplot as plt
import math

x = np.linspace(0, 14, 1000)
y = -.08*((x-4)**2) + 1

print(y)
plt.plot(x,y)
plt.ylim(ymin=0)
plt.show()