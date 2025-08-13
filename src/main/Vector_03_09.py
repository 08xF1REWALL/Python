import array

class Vector2d:
    typecode = 'd'  # 'd' = double-precision float

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __iter__(self):
        # Allows unpacking like tuple(v)
        return (i for i in (self.x, self.y))

    def __repr__(self):
        return f"Vector2d({self.x}, {self.y})"

    def __bytes__(self):
        # First byte: typecode, then packed floats
        return (bytes([ord(self.typecode)]) +
                array.array(self.typecode, self).tobytes())

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])  # first byte = typecode
        memv = memoryview(octets[1:]).cast(typecode)  # rest = numbers
        return cls(*memv)  # unpack into x, y


# Example usage
v1 = Vector2d(3.0, 4.0)
print("Original:", v1)

data = bytes(v1)  # serialize to bytes
print("Bytes:", data)

v2 = Vector2d.frombytes(data)  # deserialize
print("Deserialized:", v2)
