import math

class Vector2d:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __iter__(self):
        return (i for i in (self.x, self.y))
    
    def __abs__(self):
        return math.hypot(self.x, self.y)
    
    def angle(self):
        return math.atan2(self.y, self.x)
    
    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):  # polar coordinates
            fmt_spec = fmt_spec[:-1]  # strip 'p'
            coords = (abs(self), self.angle())
            outer_fmt = '<{}, {}>'
        else:  # Cartesian coordinates
            coords = self
            outer_fmt = '({}, {})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(*components)

# Examples
print(format(Vector2d(1, 1)))         # (1, 1)
print(format(Vector2d(1, 1), '.2f'))  # (1.00, 1.00)
print(format(Vector2d(1, 1), 'p'))    # <1.4142135623730951, 0.7853981633974483>
print(format(Vector2d(1, 1), '.3fp')) # <1.414, 0.785>
