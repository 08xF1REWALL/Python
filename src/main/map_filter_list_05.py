from math import factorial
print(list(map(factorial, range(6)))) # factorials from 0! to !5
print(list(map(factorial, filter(lambda n: n % 2, range(6))))) # map applies the factorial to each function, list warps the result in a list, so the final output is [1,6,120]
print([factorial(n) for n in range(6) if n % 2])