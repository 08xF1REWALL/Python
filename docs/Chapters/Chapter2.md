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

13. s.insert(p, e)
a = [10, 30]
a.insert(1, 20)
print(a)

14. s.__iter__()
for i in [1, 2, 3]:
print(1)

15. s.__len__()
print(len([1, 2, 3]))
print(len(('a', 'b')))

16. s.__mul__(n): repeate concatenation
a = [1, 2]
b = a * 2
print(b)  # [1, 2, 1, 2]
print(a)  # [1, 2] → original unchanged
print(a is b)  # False → different objects

17. s.__imul__(n): in place repeated concatenation
t = (1, 2)
print(id(t))
t *= 2
print(t)           # (1, 2, 1, 2)
print(id(t))       # different ID → new object


18. s.__rmul__(n) 
a = [1, 2, 3]
for item in reversed(a)
print(item)

19. s.pop([p])
a = [10, 20, 30]
print(a.pop())     # 30 (last item)
print(a.pop(0))    # 10 (item at index 0)

20. s.remove(e)
a = [10, 20, 20, 30]
a.remove(20)
print(a)  # [10, 30, 20]

21. s.reverse(): reverse item in place
a = [1, 2, 3]
a.reverse()
print(a)  # [3, 2, 1]

22. s.__reversed__(): get iterator scanning from last to first
a = [1, 2, 3]
for item in reversed(a):
print(a)

23. s.__setitem__(p, e)
a = [10, 20, 30]
a[1] = 99
print(a)

24. a = [3, 1, 2]
a.sort(a)
a.sort(reverse=true)
print(a)
words = ["apple", "banana", "cherry"]
words.sort(key=len)
print(words)

## Slicing
l = [10, 20, 30, 40, 50, 60]
l[:2]
[10, 20]
l[2:]
[30, 40, 50, 60]

```py
invoice = """
... 0.....6.................................40........52...55........
... 1909 Pimoroni PiBrella $17.50 3 $52.50
... 1489 6mm Tactile Switch x20 $4.95 2 $9.90
... 1510 Panavise Jr. - PV-201 $28.00 1 $28.00
... 1601 PiTFT Mini Kit 320x240 $34.95 1 $34.95
"""
SKU = slice(0, 6)
DESCRIPTION = slice(6, 40)
UNIT_PRICE = slice(40, 52)
QUANTITY = slice(52, 55)
ITEM_TOTAL= slice(55, none)
line_item = invoice.split('\n')[2:]
    print(item[UNIT_PRICE], item[DESCRIPTION])
```

## Multidimensional Slicing and Ellipsis

```py
l = list(range(10))
print(l)
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
l [2:5] = [20, 30]
print(l)
[0, 1, 20, 30, 5, 6, 7, 8, 9]
del l[5:7]
[0, 1, 20, 30, 5, 8, 9]

l[3::2] = [11, 22] # :: start stop

[0, 1, 20, 11, 5, 22, 9]

l [2:5] = [100]
[0, 1, 100, 22, 9]


l = [1, 2, 3]
l * 5
[1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3]

```

## Building lists of Lists
```py
board = [['_'] * 3 for i in range(3)]
[['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]

weird_board = [['_'] * 3] * 3
print(weird_board)
weird_board [1][2] = 'O'
[['_', '_', 'O'], ['_', '_', 'O'], ['_', '_', 'O']]



```

```py
board = []
for i in range(3)
    row = ['_'] * 3
    board.append(row)
for row in board:
    print(row)

```
## Augmented Assignment with sequences
```py
l = [1, 2, 3]
print(id(l))
l *= 2
print(l)
print(id(l))
t = (1, 2, 3)
print(id(t))
t *= 2
print(id(t))

```
python3 mut_unmut_seq_02.py
140161258900288
[1, 2, 3, 1, 2, 3]
140161258900288
140161257297344
140161257000672

```py
t = (1, 2, [30, 40])
t[2] += [50, 60]
print(t)
```
- find insert position with bisect

```py
import bisect # imports the bisect module for binary search
import sys # let the script read command-line arguments like left
 
HAYSTACK = [1, 4, 5, 6, 8, 12, 15, 20, 21, 23, 23, 26, 29, 30]
NEEDLES = [0, 1, 2, 5, 8, 10, 22, 23, 29, 30, 31]

ROW_FMT = '{0:2d} @ {1:2d} {2}{0:<2d}'

def demo(bisect_fn):
    for needle in reversed(NEEDLES)
    position = bisect_fn(HAYSTACK, needle)
    offset = position * ' |'
    print(ROW_FMT.format(needle, position, offset))
    
if __name__ == '__main__':
    if sys.argv[-1] == 'left':
        bisect_fn = bisect.bisect_left
    else:
        bisect_fn = bisect.bisect
    print('DEMO:', bisect_fn.__name__)
    print('haystack ->', ' '.join('%2d' % n for n in HAYSTACK))
    demo(bisect_fn)
```
algorithm: sorted lists (O(log n) time complexity)

n = is the element

log₂(14) = 3.8074 = 4 steps 
log₂(14) = ln(14) / ln(2)
eʸ = 14, eʸ = 2.
2.6390573296152584 / 0.6931471805599453 ≈ 3.807354922057604

## inserting with bisect.insort

```py
import bisect
import random

SIZE = 7 
random.seed(1729)

my_list = []
for i in range(SIZE):
    new_item = random.randrange(SIZE*2)
    print(new_item)
    bisect.insort(my_list, new_item)
    print('%2d ->' %new_item, my_list)
```

## Arrays
- Creating and saving and loading a larg array of floats

```py
import os
from array import array
from random import random

# Create an array of 10 million random floats
floats = array('d', (random() for i in range(10**7))) #'d' (double-precision float, 8 bytes each)


print(floats[-1])  # Print the last element

# Write the array to a binary file
fp = open('../../examples/floats.bin', 'wb') # write-binary mode ('wb').
floats.tofile(fp) # write the contents to file as binary data
fp.close()

# Read the array back from the file
floats2 = array('d')
fp = open('../../examples/floats.bin', 'rb') # read binary mode ('rb').
floats2.fromfile(fp, 10**7)
fp.close()
print(floats2[-1])  # Print the last element
```

## Memory Views
is a shared memory class sequence type, it let us handle slices of array without copying bytes.

array.array('h', [.....]) it create an array type code h which represent signed short integer, 2 bytes each, 16 bits, range -2^15 - 2^15 -1 -32768 - 32767
 signed short integer : -2^15 - 2^15 -1 -32768 - 32767
 unsighned byte: 0 to 255
`

```py
numbers = array.array('h', [-2, -1, 0, 1, 2])
memv = memoryview(numbers) # create memory view object, thats provide view into the memory of numbers, without copying data.
len(memv)
# Output: 5
memv[0]
# Output: -2
memv_oct = memv.cast('B') # casting to unsighed bytes 
memv_oct.tolist() # convert memoryview into py list of integers.
# Output: [254, 255, 255, 255, 0, 0, 1, 0, 2, 0]
memv_oct[5] = 4
numbers
# Output: array('h', [-2, -1, 1024, 1, 2])

```

## NumPy and Scipy
1. Numpy Methods: arange, array, zeros, random.randint, reshape, mean, save, load
2. array.array Methods: append, extend, pop, tofile, fromfile, tolist

```py
import numpy
import random
a = array.random(12)
a = numpy.arange(a)
print(a)

```

```py
import numpy as np
from array import array

# Create arrays
a_numpy = np.arange(12, dtype=np.int16)
a_array = array('h', range(12))

# Manipulate with numpy
print("Original numpy array:", a_numpy)
print("Reshaped (3x4):", a_numpy.reshape(3, 4))
print("Squared:", np.power(a_numpy, 2))
print("Mean:", a_numpy.mean())
print("Values > 5:", a_numpy[a_numpy > 5])

# Manipulate with array.array
print("\nOriginal array.array:", a_array)
a_array.append(12)
print("After append(12):", a_array)
a_array.pop()
print("After pop():", a_array)

# Save to binary file (like in array_floats_02.py)
with open('examples/a_array.bin', 'wb') as f:
    a_array.tofile(f)

# Load from binary file
a_loaded = array('h')
with open('examples/a_array.bin', 'rb') as f:
    a_loaded.fromfile(f, 12)
print("Loaded array.array:", a_loaded)

# Save numpy array
np.save('examples/a_numpy.npy', a_numpy)
```
## Numpy also supports high-level operation for loading and saving operation on all elements

```py
import numpy 
floats = numpy.loadtxt('float-10M.txt')
print(float[-3:]) 


```
## working with deque

```py
dq = deque(range(10), maxlen=10)
print(dq)
dq.rotate(3)
print(dq)
dq.rotate(-4)
dq.appendleft(-1)
print(dq)
dq.extend([11, 22, 33])
print(dq)
dq.extendleft([10, 20, 30, 40])
```

## mixed bag

l = [28, 14, '28', 5, '9', '1', 0, 6, '23', 19]
sorted(l, key=int)

## insertion sort
Outer loop: Runs from index 1 to n-1
total comparision: 1 + 2 + 3 + (n-1) = n(n-1)/2 = n^2/2
O(n^2)
n^2 is the total operation (comparisions + shifts, up to 90 in the worst case)
example : 
n = 10 
n(n-1)/2 = (100 - 10)/2 = 45 -> this will be the shifts

l = [28, 14, '28', 5, '9', '1', 0, 6, '23', 19]

comparisions n(n−1)/2=(10⋅9)2=45.
shifts n(n-1)/2 = 45
total operation 45 + 45 = 90


```py
def insertion_sort(arr, key=lamda x: x):
    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        # Compare using the key function and shift larger elements right
        while j >=0 and key(arr[j]) > key(current):
            arr[j + 1] = arr[j]
            j -=1
            arr[j + 1] = current
    return arr
l = [28, 14, '28', 5, '9', '1', 0, 6, '23', 19]
insertion_sort(l, key=int)
print("Sorted List:", l)


```

```py
def insertion_sort(arr, key=lambda x: x):
    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        while j >= 0 and key(arr[j]) > key(current):
            print(f"i={i}, j={j}, arr[j]={arr[j]}, current={current}, key(arr[j])={key(arr[j])} > key(current)={key(current)}")
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = current
    return arr

l = [28, 14, '28', 5, '9', '1', 0, 6, '23', 19]
insertion_sort(l.copy(), key=int)

```