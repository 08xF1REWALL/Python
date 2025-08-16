import functools
import operator

n = 0
for i in range(1, 6):
    n ^= i
print(n)

y = functools.reduce(lambda a, b: a^b, range(6))
x = functools.reduce(operator.xor, range(6))

print(y)