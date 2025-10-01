import numpy as np
from array import array

# Create arrays
a_numpy = np.arange(12, dtype=np.int16)
a_array = array('h', range(12))

# Manipulate with numpy
print("Original numpy array:", a_numpy)
print("Squared:", np.power(a_numpy, 2))
print("Mean:", a_numpy.mean()) # sum / count
print("Sum:", a_numpy.sum())
print("Values > 5:", a_numpy[a_numpy > 5])

# transpose
a_reshape = a_numpy.reshape((3, 4))
print("Reshaped (3x4):", a_reshape)
print("Transposed (4x3):", a_reshape.transpose())     

# Manipulate with array.array
print("\nOriginal array.array:", a_array)
a_array.append(12)
print("After append(12):", a_array)
a_array.pop()
print("After pop():", a_array)

# Save to binary file (like in array_floats_02.py)
with open('../../examples/numpy.bin', 'wb') as f:
    a_array.tofile(f)

# Load from binary file
a_loaded = array('h')
with open('../../examples/numpy.bin', 'rb') as f:
    a_loaded.fromfile(f, 12)
print("Loaded array.array:", a_loaded)

# Save numpy array
np.save('../../examples/numpy.bin', a_numpy)

# Load numpy array
a_loaded_numpy = np.load('../../examples/numpy.bin.npy')
print("Loaded numpy array:", a_loaded_numpy)
print("Last three elements_", a_loaded_numpy[-3:])
a_loaded_numpy *= 2
print("After multiplication:", a_loaded_numpy)
print("Last three elements_", a_loaded_numpy[-3:])
