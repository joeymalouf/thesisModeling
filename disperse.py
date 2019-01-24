import numpy as np
import scipy.signal
import time

molecule_arrays = np.zeros((len([1,2,3,4,5,6,7]),4,4,))
molecule_arrays[0] = [1,2,3,4]
molecule_arrays[1] = [1,1,1,1]
molecule_arrays[2][3][2] = 3

print(molecule_arrays)

filterA = np.array([[.0125, .0125, .0125],
                [.0125, .9, .0125],
                [.0125, .0125, .0125]])
a=0
yay = time.time()

for i in range(len(molecule_arrays)):
    print(molecule_arrays[i].mean())


while a < 40:
    for i in range(len(molecule_arrays)):
        molecule_arrays[i] = scipy.signal.convolve2d(molecule_arrays[i], filterA, mode='same', boundary='wrap')
        a += 1
print(time.time()-yay)
h = 10**(-7)
pH = -np.log10(h)
print(pH)
