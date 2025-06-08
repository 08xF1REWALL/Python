n = 42
print(hash(n))
print(bin(n))
print(hash(123))        # prints 123
print(hash("hello"))    # prints some integer (different each run unless fixed)
print(hash((1, 2, 3)))  # tuple hash
