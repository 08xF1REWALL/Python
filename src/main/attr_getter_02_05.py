from collections import namedtuple
university_data = [
    ('Harvard University', 'US', 21000, (42.3770, -71.1167)),
    ('University of Cambridge', 'UK', 20000, (52.2043, 0.1149)),
    ('University of Tokyo', 'JP', 28000, (35.7126, 139.7610)),
    ('University of São Paulo', 'BR', 90000, (-23.5615, -46.7300)),
    ('Delhi University', 'IN', 300000, (28.5840, 77.1638)),
]

# nametuple it's as class
Coordinates = namedtuple('Coordinates', 'lat long')
University = namedtuple('University', 'name cc studentid coord')

# instance 
universities = [
    University(name, cc, studentid, Coordinates(lat, long))
    for name, cc, studentid, (lat, long) in university_data
    ]
#for uni in universities:
print(university_data[0])
