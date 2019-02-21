import faulthandler
faulthandler.enable()
import numpy as np
import scipy.signal
import time

molecule_arrays = np.zeros((32000,32000))


print(molecule_arrays)

yay = time.time()
x = 0
while x < 1:
    molecule_arrays = molecule_arrays*.4
    x+=1
    print(x,'\r')

print(time.time()-yay)

print(molecule_arrays)