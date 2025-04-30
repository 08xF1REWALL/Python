DIAL_CODES = [
 (86, 'China'),
 (91, 'India'),
 (1, 'United States'),
 (62, 'Indonesia'),
 (55, 'Brazil'),
 (92, 'Pakistan'),
 (880, 'Bangladesh'),
 (234, 'Nigeria'),
 (7, 'Russia'),
 (81, 'Japan'),
 ]
d1 = dict(DIAL_CODES)
print('d1:', d1.keys()) # this create a dict from a list of tuples in original order
d2 = dict(sorted(DIAL_CODES)) # this create a dict from a list of tuples in sorted order by the first element of each tuple
print('d2:', d2.keys())
d3 = dict(sorted(DIAL_CODES, key=lambda x: x[1])) # this create a dict from a list of tuples in sorted order by the second element of each tuple
# this is the same as d2 but sorted by the second element of each tuple
print('d3:', d3.keys())
assert d1 == d2 and d2 == d3