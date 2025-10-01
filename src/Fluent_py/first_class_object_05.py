def factorial(n):
    '''return n!'''
    return 1 if n < 2 else n * factorial(n-1)
print(factorial(42))

def greet(name):
    return f"Hello, {name}!"
# 1. Assign to a variable
say_hello = greet
print(say_hello) # referencing the function greet without calling it.
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

