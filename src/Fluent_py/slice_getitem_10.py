import numbers

class Vector:
    def __init__(self, components):
        self._components = list(components)  # store as list

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        cls = type(self)   # get the class of the current instance
        if isinstance(index, slice):  # slicing
            return cls(self._components[index])  # return new Vector
        elif isinstance(index, numbers.Integral):  # integer index
            return self._components[index]        # return single item
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))

    def __repr__(self):
        return f"{type(self).__name__}({self._components})"

v = Vector([10, 20, 30, 40, 50])

print(len(v))       # 5
print(v[0])         # 10
print(v[-1])        # 50
print(v[1:4])       # Vector([20, 30, 40])
print(type(v[1:4])) # <class '__main__.Vector'>

class SubVector(Vector):
    pass

sv = SubVector([1, 2, 3, 4, 5])
print(sv[1:3])       # SubVector([2, 3])
print(type(sv[1:3])) # <class '__main__.SubVector'>
