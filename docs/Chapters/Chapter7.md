# Function Decorators and Closures
- decorator usually replaces a function with different one

```py
def deco(func):
    def inner():
        return inner

@deco
def target():
    print('running target()')
target()
```

## Closure

a closure is a function that retains the bindings of the free variables that
exist when the function is defined, so that they can be used later when the function is
invoked and the defining scope is no longer available.

Note that the only situation in which a function may need to deal with external variables
that are nonglobal is when it is nested in another function.

✅ Closure = Function + Remembered Variables
Let's break it down:
A closure happens when:

You have a nested function (a function defined inside another).

The inner function uses variables from the outer function's scope.

The outer function returns the inner function.


🔧 Use Cases for Closures
Function factories: Creating functions with preset behaviors.

Decorators: Functions that wrap other functions — decorators use closures heavily.

Encapsulation: Closures can hide variables without using classes.



```py
def outer(x):
    def inner(y):
        return x + y  # x is from the outer scope
    return inner

add_5 = outer(5)     # Now add_5 is a closure
print(add_5(10))     # ➜ 15


```

```py
def make_averager():
        series = []

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total/len(series)
        return averager


```


## The nonlocal Declaration 

```py
def make_averager():
    count = 0
    total = 0
    def averager(new_value):
        count += 1
        total += new_value
        return total / count
    return averager

```
✅ Why it works:
count and total are in the enclosing function's scope.

The nonlocal keyword allows the inner function to modify those variables.
❓ Why?

Python sees that you're assigning to count and total inside averager().

So it assumes they are local to averager.

But you're trying to use them before they’ve been assigned → UnboundLocalError.
The problem is that the statement count += 1 actually means the same as count when count is a number or any immutable type. So we are actually assigning
to count in the body of averager, and that makes it a local variable. 

If a new value is assigned to a nonlocal variable, the binding stored in the closure is
changed. A correct implementation of our newest make_averager looks like
```py
def make_averager():
    count = 0
    total = 0
    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total / count
    return averager

```
## Implement a Simple Decorator

A simple decorator to output the running time of functions

```py
import time

def clock(func):
    def clocked(*args):
        t0 = time.perf_counter()  # ⏱ Start time
        result = func(*args)      # Call the original function
        elapsed = time.perf_counter() - t0  # ⏱ Time taken

        name = func.__name__      # Function name
        arg_str = ', '.join(repr(arg) for arg in args)  # Arg string

        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result

    return clocked

@clock
def add(x, y):
    return x + y
add(10, 20)

```

```py
import time
from deco_run_time_func_07 import clock

@clock
def snooze(seconds):
    time.sleep(seconds)

@clock
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)

if __name__=='__main__':
 print('*' * 40, 'Calling snooze(.123)')
 snooze(.123)
 print('*' * 40, 'Calling factorial(6)')
print('6! =', factorial(6))    

```

```py
@clock
def factorial(n):
 return 1 if n < 2 else n*factorial(n-1)
# Actually does this:

def factorial(n):
 return 1 if n < 2 else n*factorial(n-1)
factorial = clock(factorial)

```

## Decorators in the Standard Library

py has three build in func that are designed to decorate methods: property, classmethod, staticmethod

## Memoization with functools.lru_cache

A very practical decorator is functools.lru_cache. It implements memoization: an
optimization technique that works by saving the results of previous invocations of an
expensive function, avoiding repeat computations on previously used arguments. The
letters LRU stand for Least Recently Used, meaning that the growth of the cache is
limited by discarding the entries that have not been read for a while.

```py
#import functools
from deco_run_time_func_07 import clock

#@functools.lru_cache()
@clock 
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2) + fibonacci(n-1)
if __name__=='__main__':
    print(fibonacci(30))
    
```

## Stacked Decorators

```py
@d1
@d2
def f():
    print('f')

# same as 
def f():
    print('f')
f = d1(d2(f))
```
## Parameterized Decorators

```py

registry = []

def registry(func):
    print('running register(%s)' % func)
    registry.append(func)
    return func

@register
def f1():
    print('running f1()')
print('running main()')
print('registry ->', registry)
f1()
```