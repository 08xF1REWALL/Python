from Vector_09 import Vector2d
@classmethod # decorator a class method
def frombytes(cls, octets): # octets is expected to be a bytes or bytesarray obj containing serialized vector
    typecode = chr(octets[0])
    memv = memoryview(octets[1:]).cast(typecode) # memoryview creates a zero copy view of the binary data meaning no memory allocation happens
    return cls(*memv) #unpacking the memv into seperate arguments in this case (3.0, 4.0)

