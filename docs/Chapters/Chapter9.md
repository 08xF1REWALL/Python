# A Pythonic Object
## Vector Class Redux

```py
import array

class Vector2d:
    typecode = 'd'  # Indicates double precision float

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    
    def __iter__(self):
        yield self.x  # Generator method to iterate over x, y
        yield self.y

    def __repr__(self):
        return f"Vector2d({self.x}, {self.y})"

    def __eq__(self, other):
        return isinstance(other, Vector2d) and self.x == other.x and self.y == other.y

    def __bytes__(self):
        return bytes(array.array(self.typecode, [self.x, self.y]))  # Use array to pack floats

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __bool__(self):
        return bool(self.x or self.y)

v1 = Vector2d(3, 4)
print(v1.x, v1.y)          # 3.0 4.0
v1_clone = eval(repr(v1))
print(v1 == v1_clone)      # True
octets = bytes(v1)
print(octets)              # b'\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@' (8 bytes for each float)
print(v1)                  # (3.0, 4.0)
print(bool(v1), bool(Vector2d(0, 0)))  # True False

```

```py
@classmethod
def frombytes(cls, octets):
    typecode = chr(octets[0])
    memv = memoryview(octets[1:]).cast(typecode)
    return cls(*memv)
    
```
