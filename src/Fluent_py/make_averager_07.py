def make_averager():
    count = 0
    total = 0
    def averager(new_value):
        nonlocal count, total  # Required to modify enclosing scope variables
        count += 1
        total += new_value
        return total / count
    return averager
avg = make_averager() # assigning the function, not calling it
print(avg(19))