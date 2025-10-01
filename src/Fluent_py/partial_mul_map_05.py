from operator import mul
from functools import partial
triple = partial(mul, 3)
print(triple(8))
print(list(map(triple, range(1, 10))))