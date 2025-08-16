# Assuming you already have this Vector class with _components
from array import array
import functools
import operator

class Vector:
    typecode = 'd'

    def __init__(self, components):
        self._components = list(components)

    def __iter__(self):
        return iter(self._components)

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __hash__(self):
        hashes = (hash(x) for x in self._components)
        return functools.reduce(operator.xor, hashes, 0)
    """"hashes is a generator, meaning it computes each hash(x) lazily, one at a time.

functools.reduce(operator.xor, hashes, 0) starts with 0 as the initial value and XORs each hash in turn.

Advantage: Memory efficient (doesn’t store the whole list).

The 0 initial value ensures that an empty vector will have hash = 0.
 Latest code (using map())"""

    def __repr__(self):
        return f"Vector({self._components})"


# ===== TESTS WITH HASH PRINTS =====

v1 = Vector([1.0, 2.0, 3.0])
v2 = Vector([1.0, 2.0, 3.0])
v3 = Vector([3.0, 4.0, 5.0])
v4 = Vector([0.0, 0.0, 0.0])

# Print vectors and their hashes
print("v1:", v1, "hash:", hash(v1))
print("v2:", v2, "hash:", hash(v2))
print("v3:", v3, "hash:", hash(v3))
print("v4:", v4, "hash:", hash(v4))

# Test equality
print("\nEquality tests:")
print("v1 == v2:", v1 == v2)   # True
print("v1 == v3:", v1 == v3)   # False
print("v1 == v4:", v1 == v4)   # True

# Test hashing in a set
print("\nSet membership tests:")
s = {v1, v3}
print("v2 in set:", v2 in s)   # True, because v2 equals v1
print("v3 in set:", v3 in s)   # True
print("v4 in set:", v4 in s)   # False

# Test hashing as dict keys
print("\nDictionary key tests:")
d = {v1: "A point", v3: "Another point"}
print("d[v2]:", d[v2])  # "A point"
print("d[v3]:", d[v3])  # "Another point"

# Test consistency of hash and equality
print("\nHash consistency checks:")
print("hash(v1) == hash(v2):", hash(v1) == hash(v2))  # True
print("hash(v1) == hash(v3):", hash(v1) == hash(v3))  # Usually False
print("hash(v1) == hash(v4):", hash(v1) == hash(v4))  # Usually False
