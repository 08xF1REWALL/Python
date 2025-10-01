class Vector:
    shortcut_names = 'xyzt'

    def __init__(self, components):
        self._components = list(components)

    def __getattr__(self, name):
        cls = type(self)
        if len(name) == 1:
            pos = cls.shortcut_names.find(name)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, name))

    def __repr__(self):
        return f"{type(self).__name__}({self._components})"

v2 = Vector([3, 4])
print(v2.x)   # 3
print(v2.y)   # 4
# print(v2.z) # AttributeError: 'Vector' object has no attribute 'z'

v3 = Vector([1, 2, 3])
print(v3.z)   # 3
