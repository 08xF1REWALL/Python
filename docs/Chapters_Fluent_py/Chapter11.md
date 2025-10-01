# Interfaces: From Protocols to ABCs

The abc (Abstract Base Classes) module is part of Python’s standard library.

It lets you define abstract base classes (ABCs).

An abstract base class is like a blueprint: it defines methods/properties that must be implemented by any subclass.

You cannot instantiate an abstract class directly.

Exception error Types:
BaseException
├── SystemExit
├── KeyboardInterrupt
├── GeneratorExit
└── Exception
 ├── StopIteration
 ├── ArithmeticError
 │ ├── FloatingPointError
 │ ├── OverflowError
 │ └── ZeroDivisionError
 ├── AssertionError
 ├── AttributeError
 ├── BufferError
 ├── EOFError
 ├── ImportError
 ├── LookupError
 │ ├── IndexError
 │ └── KeyError
 ├── MemoryError
 ... etc.

```py
from tombola import Tombola
class Fake(Tombola):
    def pick(self):
        return 13
```

## ABC syntax Details & Subclassing the Tombola ABC
class Tombola(metaclass=abc.ABCMeta):

```py
import random
from tombola import Tombola
class BingoCage(Tombola):
    def __init__(self, item):
        self._randomizer = random.SystemRandom()
        self._item = []
        self.load(item)

    def load(self, item)
    self._items.extend(items)
    self._randomizer.shuffle(self._items)

    def pick(self):
        try:
            return self._item.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')
    
    def call(self):
        self.pick()
```
