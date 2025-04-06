# The Python Data Model

## Emulating Numeric types

```py
v1 = Vector(2, 4)
v2 = Vector(2, 1)
v1 + v2
abs(v1) # abs return the absolute value of int and float and complex num
v1 * 3

```

```py
from math import hypot
class Vector:
    
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __repr__(self): # get the strin representation of the object
        return 'Vector(%r, %r)' % (self.x, self.y)
    
    def __abs__(self):
        return hypot(self.x, self.y)
    
    def __bool__(self):
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
```

## Special method names

1. String/bytes representation __repr__, __str__, __format__, __bytes__
2. Conversion to number __abs__, __bool__, __complex__, __int__, __float__, __hash__,
__index__
3. Emulating collections __len__, __getitem__, __setitem__, __delitem__, __contains__
4. Iteration __iter__, __reversed__, __next__
5. Emulating callables __call__
6. Context management __enter__, __exit__
7. Instance creation and destruction __new__, __init__, __del__
8. Attribute management __getattr__, __getattribute__, __setattr__, __delattr__, __dir__
9. Attribute descriptors __get__, __set__, __delete__
10. Class services __prepare__, __instancecheck__, __subclasscheck__

## special method names of operators
1. Unary numeric operators __neg__ -, __pos__ +, __abs__ abs()

2. Rich comparison operators __lt__ >, __le__ <=, __eq__ ==, __ne__ !=, __gt__ >, __ge__ >=

3. Arithmetic operators __add__+, __sub__ -, __mul__ *, __truediv__ /, __floordiv__ //, __mod__
%, __divmod__ divmod() , __pow__ ** or pow(), __round__ round()

4. Reversed arithmetic operators __radd__,__rsub__,__rmul__,__rtruediv__,__rfloordiv__,__rmod__,
__rdivmod__, __rpow__

5. Augmented assignment arithmetic operators
__iadd__,__isub__,__imul__,__itruediv__,__ifloordiv__,__imod__,
__ipow__

6. Bitwise operators __invert__ ~, __lshift__ <<, __rshift__ >>, __and__ &, __or__ |,
__xor__ ^

7. Reversed bitwise operators __rlshift__, __rrshift__, __rand__, __rxor__, __ror__

8. Augmented assignment bitwise operators
__ilshift__, __irshift__, __iand__, __ixor__, __ior__

```py
class BitwiseExample:
    def __init__(self, value):
        self.value = value

    def __ilshift__(self, other):
        self.value <<= other
        return self

    def __irshift__(self, other):
        self.value >>= other
        return self

    def __iand__(self, other):
        self.value &= other
        return self

    def __ixor__(self, other):
        self.value ^= other
        return self

    def __ior__(self, other):
        self.value |= other
        return self

    def __repr__(self):
        return str(self.value)

# Example Usage
num = BitwiseExample(6)
num &= 3
print(num)  # Output: 2

```