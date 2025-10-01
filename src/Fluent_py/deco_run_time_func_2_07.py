import time

DEFAULT_FMT= '[{elapsed:0.8f}s] {name}({args}) -> {result}'

def clock(fmt=DEFAULT_FMT):
    def decorate(func):
        def clocked(*args):
            t0 = time.perf_counter()  # ⏱ Start time
            _result = func(*args)      # Call the original function
            elapsed = time.perf_counter() - t0  # ⏱ Time taken
            name = func.__name__      # Function name
            arg_str = ', '.join(repr(arg) for arg in args)  # Arg string
            result = repr(_result)
            print(fmt.format(**locals()))
            return _result
        return clocked
    return decorate
if __name__ == '__main__':
    
    @clock()
    def snooze(seconds):
        time.sleep(seconds)
    
    for i in range(3):
        snooze(.123)            
