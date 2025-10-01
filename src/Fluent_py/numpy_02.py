import numpy as np
from array import array
import random
a_array = array('h', (random.randint(-100,100) for _ in range(12)))
print("array.array (random):", a_array)

b_array = np.random.randint(-100, 100, size=12, dtype=np.int16)
print("numpy (random):", b_array)

a_numpy_from_array = np.array(a_array, dtype=np.int16)
print("numpy from array:", a_numpy_from_array)