from collections import namedtuple

# Raw data
metro_data = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('São Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]

# Define namedtuples
LatLong = namedtuple('LatLong', 'lat long')
Metropolis = namedtuple('Metropolis', 'name cc pop coord')

# Build a list of Metropolis instances with LatLong as coordinates
metro_areas = [Metropolis(name, cc, pop, LatLong(lat, long))
               for name, cc, pop, (lat, long) in metro_data]

# Example: print all metro_areas
for city in metro_areas:
    print(city)

# Example: print the first raw tuple
print("\nRaw tuple from metro_data:")
print(metro_data[0])
