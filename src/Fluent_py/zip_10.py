class VectorVerbose:
    """Vector with the verbose __eq__"""
    def __init__(self, components):
        self._components = list(components)

    def __iter__(self):
        return iter(self._components)

    def __len__(self):
        return len(self._components)

    # Verbose __eq__
    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for a, b in zip(self, other):
            if a != b:
                return False
        return True


class VectorPythonic:
    """Vector with the pythonic __eq__"""
    def __init__(self, components):
        self._components = list(components)

    def __iter__(self):
        return iter(self._components)

    def __len__(self):
        return len(self._components)

    # Pythonic __eq__
    def __eq__(self, other):
        return len(self) == len(other) and all(a == b for a, b in zip(self, other))


# ==== TESTS ====

v1 = VectorVerbose([1, 2, 3])
v2 = VectorVerbose([1, 2, 3])
v3 = VectorVerbose([1, 2])
v4 = VectorVerbose([1, 2, 4])
v5 = VectorVerbose([])

p1 = VectorPythonic([1, 2, 3])
p2 = VectorPythonic([1, 2, 3])
p3 = VectorPythonic([1, 2])
p4 = VectorPythonic([1, 2, 4])
p5 = VectorPythonic([])

print("===== Verbose __eq__ Tests =====")
print("v1 == v2 (equal vectors):", v1 == v2)  # True
print("v1 == v3 (different lengths):", v1 == v3)  # False
print("v1 == v4 (same length, different values):", v1 == v4)  # False
print("v5 == v5 (both empty):", v5 == v5)  # True

print("\n===== Pythonic __eq__ Tests =====")
print("p1 == p2 (equal vectors):", p1 == p2)  # True
print("p1 == p3 (different lengths):", p1 == p3)  # False
print("p1 == p4 (same length, different values):", p1 == p4)  # False
print("p5 == p5 (both empty):", p5 == p5)  # True

print("\n===== Cross-check behavior is identical =====")
print("v1 == v2:", v1 == v2, " | p1 == p2:", p1 == p2)
print("v1 == v3:", v1 == v3, " | p1 == p3:", p1 == p3)
print("v1 == v4:", v1 == v4, " | p1 == p4:", p1 == p4)
print("v5 == v5:", v5 == v5, " | p5 == p5:", p5 == p5)
