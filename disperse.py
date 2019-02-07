import faulthandler
faulthandler.enable()
import numpy as np
import scipy.signal
import time
# import tensorflow as tf

molecule_arrays = np.zeros((19,19))
molecule_arrays[10][10] = 10000


print(molecule_arrays)

filterA = np.array([[.0125, .0125, .0125],
                [.0125, .9, .0125],
                [.0125, .0125, .0125]])
filterB = np.array([[.025, .025, .025],
                [.025, .8, .025],
                [.025, .025, .025]])
a=0
yay = time.time()



while a < 40:
    molecule_arrays = scipy.signal.convolve2d(molecule_arrays, filterA, mode='same', boundary='wrap')
    a += 1
print(time.time()-yay)
h = 10**(-7)
pH = -np.log10(h)
print(molecule_arrays)
print(molecule_arrays[10][10])

# array = np.random.random((100,100))
# print("test")
# filterA = np.array([[.0125, .0125, .0125],
#                 [.0125, .9, .0125],
#                 [.0125, .0125, .0125]])
# scipyArray = scipy.signal.convolve2d(array, filterA, mode='same', boundary='wrap')
# start = time.time()
# print("scipy 2d:" + str(time.time()-start))

# sess = tf.Session()
# tfArray = tf.nn.conv2d(np.expand_dims(np.expand_dims(array, axis=0), axis=3),
#                         np.expand_dims(np.expand_dims(np.rot90(filterA,2),axis=3),axis=4),
#                         strides=[1,1,1,1],padding="VALID",
#                         dilations=[1,1,1,1])
                    
# tfresults = sess.run(tfArray)