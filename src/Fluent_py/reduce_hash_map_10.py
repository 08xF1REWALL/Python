import functools
import operator

class Vector:
    def __init__(self, components):
        self._components = list(components)

    def __iter__(self):
        return iter(self._components)

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __hash__(self):
        hashes = map(hash, self._components)
        return functools.reduce(operator.xor, hashes)
    
    """"hashes is a map object, which is very similar to a generator: it computes hash(x) lazily.

functools.reduce(operator.xor, hashes) does not provide an initial value.

This works fine if the vector is non-empty.

But if _components is empty, reduce() will raise a TypeError because it has no values to reduce."""

    def __repr__(self):
        return f"Vector({self._components})"


# ===== TESTS =====

v1 = Vector([1, 2, 3])
v2 = Vector([1, 2, 3])
v3 = Vector([3, 2, 1])
v4 = Vector([0, 0, 0])

# Test equality
print("v1 == v2:", v1 == v2)   # True
print("v1 == v3:", v1 == v3)   # False
print("v1 == v4:", v1 == v4)   # False

# Print hashes
print("\nHashes:")
print("hash(v1):", hash(v1))
print("hash(v2):", hash(v2))
print("hash(v3):", hash(v3))
print("hash(v4):", hash(v4))

# Test set membership
s = {v1, v3}
print("\nSet membership:")
print("v2 in set:", v2 in s)  # True, same as v1
print("v3 in set:", v3 in s)  # True
print("v4 in set:", v4 in s)  # False

# Test dict keys
d = {v1: "A point", v3: "Another point"}
print("\nDictionary key access:")
print("d[v2]:", d[v2])  # "A point"
print("d[v3]:", d[v3])  # "Another point"

# Check hash consistency with equality
print("\nHash consistency:")
print("hash(v1) == hash(v2):", hash(v1) == hash(v2))  # True
print("hash(v1) == hash(v3):", hash(v1) == hash(v3))  # Could be True/False depending on XOR
