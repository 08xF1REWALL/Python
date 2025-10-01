class Averager():
    def __init__(self):
        self.series = []
    
    def __call__(self, new_value):
        self.series.append(new_value)
        total = sum(self.series)
        return total/len(self.series)
    
avg = Averager()
print(avg(10))
    
def make_averager():
    series = []  # Enclosing variable

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total / len(series)

    return averager  # Return the inner function (closure)
