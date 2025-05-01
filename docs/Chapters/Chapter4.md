# Text versus Bytes

- converting from code point to bytes is encoding, and converting from bytes to code points is decoding


```py
a = 'café' # this é is not a ASCII, and UTF-8 uses two bytes to represent it \xc3\xa9
print(len(a))       # 4 characters
b = a.encode('utf8')
print(b)            # b'caf\xc3\xa9'
print(len(b))       # 5 bytes

```

- byte sequence as bytes and as bytearray

```py
cafe = bytes('Café', encoding='utf_8')
print(cafe)
print(cafe[0]) # ASCII -> hex -> decimal
print(cafe[:1]) # gives a slice of the first byte as bytes object "b'c'"
cafe_arr = bytearray(cafe) # mutable version of byte
print(cafe_arr)
print(cafe_arr[-1:]) # gives a slice of the last byte of the bytearray

```

- initializing bytes from the row data of an array

```py
import array
numbers = array.array('h', [-2, -1, 0, 1, 2])
octets = bytes(numbers)
print(octets)

```

- Structs and Memory Views

struct module provides a function to parse packed bytes into a tuble of fields of different types and to preform opposite conversion, from tuple into packed bytes.

```py
import struct
fmt = '<3s3sHH' # little-endian; 3s3s two sequences of 3 bytes; HH two 16-bit integers
with open('filter.gif', 'rb') as fp:
    img = memoryview(fp.read())
header = img[:10]
print(bytes(header))
struct.unpack(fmt, header)

```