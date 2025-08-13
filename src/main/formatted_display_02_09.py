from datetime import datetime

now = datetime.now()
print(format(now, '%H:%M:%S'))
print("It's now {:%I:%M %p}".format(now))

class Vector2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __iter__(self):
        return (i for i in (self.x, self.y))
    
    """def __format__(self, fmt_spec=''):
        coords = (format(self.x, fmt_spec), format(self.y, fmt_spec))
        return f'({coords[0]}, {coords[1]})'
    """
    def __format__(self, fmt_spec=''):
        components = (format(c, fmt_spec) for c in self) # Use the format built-in to apply the fmt_spec to each vector component, building an iterable of formatted strings.

        return '({}, {})'.format(*components) #Plug the formatted strings in the formula '(x, y)'

    
v1 = Vector2d(3, 4)
print(format(v1))         # (3, 4)
print(format(v1, '.2f'))  # (3.00, 4.00)
print(format(v1, '.3e'))  # (3.000e+00, 4.000e+00)

