import os
from array import array
from random import random

# Create an array of 10 million random floats
floats = array('d', (random() for i in range(10**7))) #'d' (double-precision float, 8 bytes each)


print(floats[-1])  # Print the last element

# Write the array to a binary file
fp = open('../../examples/floats.bin', 'wb') # write-binary mode ('wb').
floats.tofile(fp) # write the contents to file as binary data
fp.close()

# Read the array back from the file
floats2 = array('d')
fp = open('../../examples/floats.bin', 'rb') # read binary mode ('rb').
floats2.fromfile(fp, 10**7)
fp.close()
print(floats2[-1])  # Print the last element
print(floats2 == floats)
