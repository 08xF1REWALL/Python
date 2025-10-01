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