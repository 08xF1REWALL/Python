import functools
i = 2 * 3 * 4 * 5
print(i)

y = functools.reduce(lambda a,b: a*b, range(1,6))
print(y)