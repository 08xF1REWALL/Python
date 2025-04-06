# An Array of Sequences
## Overview of build in sequences

1. Container sequences: hold references to the object they contain, which may be of any type
list, tuble, and collections.deque can hold items of deferent types.
2. Flat sequences: physically store the value of each item with in it's own memory
str, bytes, bytearray, memoryview, and array.

- Mutable sequences :
list, bytearray, array.array, collection.deque, and memoryview
- Immutable sequences
tuble, str, bytes

- build a list of unicode codepoints from a string

```py
symbols = '$¢£¥€¤'
code = []
for symbol in sympols:
    code.append(ord(symbol))
print(code)

# for better readability
symbols = '$¢£¥€¤'
    code = [ord(symbol) for symbol in symbols]
print (code)
```

## Listcomps No loger leak their Variables
- here we should avoid use the same variable name as in 

```py

x = 'my precious'
dummy = [x for x in 'ABC']
x 
'C'
#it leaks the value of the last value after the itration
#python3

x = 'ABC'
dummy = [ord(x) for x in x]
x 
'ABC'

```

## Generator Expression

tuple: stand for ordered lists of element, it has specific order, once created you can't change the contents, it can also store multiable values of any type.

- Initializing a tuple of genexps to build a tuple and an array.

```py
symbols = '$¢£¥€¤'
tuple(ord(symbol) for symbol in symbols)

#########
import array
symbols = '$¢£¥€¤'
array.array('I', (ord(symbol) for symbol in symbols))

```

- Cartesian product in a generator expression

1. Generator Expression vs List Comprehension
    1.1 list Comprehension creates and stroes the entire list in memory at once
    . It returns a list

    1.2 gernerator Expression dose not store the entire list in the memory, it generates items one at time and yields them when needed
    . It returns a generator object

```py
# List comprehension
color = ['black', 'White']
size = ['S', 'M', 'L']

for tshirt in ('%s %s' % (c, s) for c in colors for s in sizes):
    print(tshirt)

####
# Generator expression
color = ['Black', 'White']
size = ['S', 'M','L']
gen_exp = ('%s %s' % (c, s) for c in color for s in size)
for item in gen_exp:
print(item)
```

## Tuple unpacking
tuple parallel assignment, is to assign item from an iterable to a tuple of variables
```py
lax_coordinates = (33.94, -118.40)
latitude, longitude = lax_coordinates # tuple unpacking
print (latitude)
print (longitude)
# or swapping the values of variables without using a temporary var
b, a = a, b

```
- tuple unpacking to return multiple values. os.path.split() function it returns a string representation of a file or directory path

```py

import os 

path = "/home/user/document/report.pdf"
print("Head:", head)
print("Tail:", tail)

```


```py
a, b, *rest = range(5)
(0, 1, [2, 3, 4])

a, *b, c = range(5)
# a = 0, b = [1, 2, 3], c = 4


```


## Nested Tuple unpacking
```py
metro_areas = [
    ('Tokyo', 'JP', 36,93, (35.68, 139.69)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]
print('{:15} | {:^9} | {:^9}'.format('', 'lat.', 'long.'))
fmt = '{:15} | {:^9.4f} | {:9.4f}'
for name, cc, pop, (latitude, longitude) in metro_areas:
    if longitude <=0:
        print(fmt.format(name, latitude, longitude))
```

```py
City._fields # acces the fields this show all names in the city tuple
('name', 'country', 'population', 'coordinates')
LatLong = namedtuple('LatLong', 'lat long') # crate a name tuple, this creates a Latlong nametuple with fields
delhi_data = ('Delhi NRC', 'IN', '21.935', LatLong(28.61, 77.20)) # define the data 
delhi = City._make(delhi_data) # create a name tuple instance, make is a class method of name tuple that lets you create a name tuple for sequence like list or tuple
delhi._asdict() # convert to a dictionary
OrderedDict([('name', 'Delhi NCR'), ('country', 'IN'), ('population', 21.935), ('coordinates', LatLong(lat=28.61, long=77,20))]) # turn the namedtuple into an orderdict
for key, value in delhi._asdict().items():
    print(key + ':', value)
```


## Tuples as Immutable lists

1. __add__: concatenation works with list and tuple
# List
a = [1, 2]
b = [3, 4]
print(a + b)  # [1, 2, 3, 4]

# Tuple
t1 = (1, 2)
t2 = (3, 4)
print(t1 + t2)  # (1, 2, 3, 4)

2. s.__iadd__(s2): tuple dose not support +=
a = [1, 2]
a += [3, 4]
print(a)  # [1, 2, 3, 4] 

3. s.append(e): append one element after the last
a = [1, 2]
a.append(3)
print(a)  # [1, 2, 3]

4. s.clear: delete all items
a = [1, 2, 3]
a.clear()
print(a)  # []

5. s.__contains__(e)
print(2 in [1, 2, 3]) # true
print("a" in ("a", "b")) # true

6. s.copy 
a = [1, 2, 3]
b = a.copy
print(b)  # [1, 2, 3]

7. print([1, 2, 2, 4].count(2)) #2
print (("x", "y", "x").count("x")) #2

8. s.__delitem__(p)
a = [10, 20, 30]
del a[1]
print(a)  # [10, 30]

9. s.extend(it)
a = [1, 2]
a.extend([3, 4])
print(a)  # [1, 2, 3, 4]

10. s.__getitem__(p)
print([10, 20, 30][1]) #20
print(["a", "b", "c"][2]) #c

11. s.__getnewargs__()
from collections import namedtuple
Point = nametuple("Point", "x y")
p = Point(1, 2)
print(p.__getnewargs__())

12. s.index(e)
print([10, 20, 30].index(20))
print(["a", "b", "c"].index("a"))