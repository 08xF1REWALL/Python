import numbers

class Vector:
    shortcut_names = 'xyzt'

    def __init__(self, components):
        self._components = list(components)

    # read-only attribute access (x, y, z, t)
    def __getattr__(self, name):
        cls = type(self)
        if len(name) == 1:  # only single-char shortcuts
            pos = cls.shortcut_names.find(name)
            if 0 <= pos < len(self._components): #pos = "xyzt".find("x") → 0
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, name))

    # prevent setting certain attributes
    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:  # single-char attributes
            if name in cls.shortcut_names:
                error = 'readonly attribute {attr_name!r}'
            elif name.islower():
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        super().__setattr__(name, value)  # normal assignment

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])  # return new Vector
        elif isinstance(index, numbers.Integral):
            return self._components[index]  # return raw element
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))

    def __repr__(self):
        return f"{type(self).__name__}({self._components})"


# ------------------ TESTS ------------------
v2 = Vector([3, 4])
print(v2)          # Vector([3, 4])
print(v2.x)        # 3
print(v2.y)        # 4
# print(v2.z)      # AttributeError: 'Vector' object has no attribute 'z'

v3 = Vector([1, 2, 3])
print(v3)          # Vector([1, 2, 3])
print(v3.z)        # 3

# Test immutability of shortcuts
try:
    v3.x = 100
except AttributeError as e:
    print(e)       # readonly attribute 'x'

# Test lowercase single-letter block
try:
    v3.a = 200
except AttributeError as e:
    print(e)       # can't set attributes 'a' to 'z' in 'Vector'

# Allowed attribute
v3.label = "point A"
print(v3.label)    # point A

# Test slicing
print(v3[0])       # 1
print(v3[1:3])     # Vector([2, 3])
