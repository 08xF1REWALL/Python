import array  # Import the array module to handle binary representation of floats

class Vector2d:
    typecode = 'd'  # Class attribute indicating the typecode for double-precision float (8 bytes)

    def __init__(self, x, y):
        self.x = float(x)  # Convert x to float and store it as an instance attribute
        self.y = float(y)  # Convert y to float and store it as an instance attribute
    
    def __iter__(self):
        yield self.x  # Yield x as part of a generator to make the object iterable
        yield self.y  # Yield y to complete the iteration over x and y coordinates

    def __repr__(self):
        return f"Vector2d({self.x}, {self.y})"  # Return a string representation for debugging/recreation

    def __eq__(self, other):
        return isinstance(other, Vector2d) and self.x == other.x and self.y == other.y
        # Check if other is a Vector2d instance and if x and y coordinates match for equality

    def __bytes__(self):
        return bytes(array.array(self.typecode, [self.x, self.y]))  
        # Convert x and y floats to bytes using the typecode 'd' (double precision), returning 16 bytes total

    def __str__(self):
        return f"({self.x}, {self.y})"  # Return a user-friendly string representation

    def __bool__(self):
        return bool(self.x or self.y)  # Return True if either x or y is non-zero, False otherwise

v1 = Vector2d(3, 4)  # Create a Vector2d instance with coordinates (3, 4)
print(v1.x, v1.y)    # Print the x and y attributes: 3.0 4.0

v1_clone = eval(repr(v1))  # Use eval on the repr string to create a new Vector2d instance
print(v1 == v1_clone)      # Compare v1 with v1_clone: True because they have identical coordinates

octets = bytes(v1)         # Convert v1 to bytes using __bytes__, resulting in a 16-byte binary representation
print(octets)              # Print the byte string: b'\x00\x00\x00\x00\x00\x00\x08@\x00\x00\x00\x00\x00\x00\x10@'
                           # (8 bytes for 3.0, 8 bytes for 4.0 in IEEE 754 double-precision format)

print(v1)                  # Print the string representation of v1: (3.0, 4.0)

print(bool(v1), bool(Vector2d(0, 0)))  # Print boolean values: True for v1 (3.0 or 4.0 is non-zero),
                                       # False for Vector2d(0, 0) (both 0.0 and 0.0 are zero)