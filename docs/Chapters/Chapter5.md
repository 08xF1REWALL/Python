# First-Class Functions
Functions in Python are first objects. Programming language theories define a "first-class object" as programm entity that can be
1. create at runtime
2. Assigend to a variable or element in a data structure
3. Passed as an argument to a function
4. Returned as the result of a function



```py
def factorial(n):
    '''return n!'''
    return 1 if n < 2 else n * factorial(n-1)
print(factorial(42))

def greet(name):
    return f"Hello, {name}!"
# 1. Assign to a variable
say_hello = greet
print(say_hello)
print(say_hello("Alice"))

# 2. Pass as an argument
def call_func(func, name):
    return func(name)
print(call_func(greet, "Bob"))

# 3. Return from another function
def get_greeting():
    return greet

greeter = get_greeting()
print(greeter("Charlie"))



```

## Modern Replacements for map, filter, and reduce

```py
list(map(fact, range(6))) # factorials from 0! to !5
list(map(factorial, filter(lambda n: n % 2, range(6)))) # map applies the factorial to each function, list warps the result in a list, so the final output is [1,6,120]
[factorial(n) from n in range(6) if n % 2]

```
in Python map and filter return generators a for of iterator, so thier direct substitute is now a generator expression

- reduce is a function used to reduce a sequence of elements into a singal value by repeatedly applying a function to the elements

- add is imported to avoid creating a function just to add two numbers
```py
from functools import reduce 
from operator import add 
reduce(add, range(100))
nums = [1, 2, 3, 4]
result = reduce(lambda x, y: x + y, nums)
print(result)

```

## Ananymous Functions 

The lambda keyword creates an anonymous function within a Python expression

```py
fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
sorted(fruits, key=lambda word: word[::-1]) # word[start:stop:step] start where slice begins default = 0, stop where the slice ends default end of the starting. Step how to move through the string -1 means go backwards

```