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

## slicing with word[start:stop:step]

1. word[::1] full string default step
2. word[::-1] Reverse string
3. word[1:4] substring from index 1 to 4
4. word[:3] from start to index 2
5. word[3:] from index 3 to end
6. word[::2] every second character
7. word[1::2] every second character starting for index 1
8. word[::-2] every second character in reverse 
9. word[-1] last character
10. word[-3:] last 3 characters
12. word[:-3] all except the last 3 characters
13. word[1:5:2] from index 1 to 4 every second character
14. word[5:2:-1] from index 5 to index 3 (reverse)

## The Seven Flavors of callable objects
1. User defined functions : Create with def statments or lambda expressions
2. Build in functions: A function implemented in c like len or time.strtime
3. Build in methods: Method implemented in C like dict.get
4. Methods: functions defined in the body of a class
5. Classes: when invoked the class run its __new__ method to create an instance, the in __init__ to initialize ot, and the finally the instance is returned to the caller.
6. Class instances : If a class definies __call__ method, then its instance may be invoiked as functions.
7. Generatorr functions : Functions or methods that use the yield keyword. When called, generator functions return a generator object.

- To determine wether if an object is callable in py, we use the callable() build in:

```py
print(abs, str, 13)
print([callable(obj) for obj in (abs, str, 13)])

```
## User-Defined Callable Types: 

## Function Introspection

## From Positional to Keyword-Only Parameters

## Retrieving Information about Parameters
using bobo Bobo web framework, which helps build web APIs 
to run 
1. bobo -f bobo.py
2. curl -i http://localhost:8080/?person=Ali
```py
import bobo
@bobo.query('/') # decoder that tells bobo when someone visit the URL path / call hello function 
def hello(person):
 return 'Hello %s!' % person

```

- Function to shorten a string by clipping at a space near the desired length

```py
def clip(text, max_len=80)
"""Return text clipped at the last space before or after max_len
 """
end = None
if len(text) > max_len:
    space_before = text.rfind(' ', 0, max_len) # space before the limit
    if space_before >= 0:
        end = space_before
    else:
        space_after = text.rfind(' ', max_len) # if space after the limit
        if space_after >= 0:
            end = space_after
if end is None: # no spaces were found
    end = len(text)
    return text[:end].rstrip()


```