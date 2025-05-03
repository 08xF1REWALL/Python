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
s = struct.unpack(fmt, header)
print (s[1])
print (s[2])
print (s[3])
print (s[4])

```

## Basic Encoders/Decoders

utf8, utf-8, U8

```py
for codec in ['latin_1', 'utf_8', 'utf_16']:
    print(codec, 'El Niño'.encode(codec), sep='\t')

```

## Handling Text Files

```py
import os

# Step 1: Write 'café' to a file with UTF-8 encoding
fp = open('cafe.txt', 'w', encoding='utf_8')
expression = "fp"
value = fp
print(expression.rjust(30), '->', repr(value))
expression = "fp.write('café')"
value = fp.write('café')
print(expression.rjust(30), '->', repr(value))
fp.close()

# Step 2: Check the file size
expression = "os.stat('cafe.txt').st_size"
value = os.stat('cafe.txt').st_size
print(expression.rjust(30), '->', repr(value))

# Step 3: Read the file with default encoding (cp1252 on Windows)
fp2 = open('cafe.txt')  # Default encoding (e.g., cp1252 on Windows)
expression = "fp2"
value = fp2
print(expression.rjust(30), '->', repr(value))
expression = "fp2.encoding"
value = fp2.encoding
print(expression.rjust(30), '->', repr(value))
expression = "fp2.read()"
value = fp2.read()
print(expression.rjust(30), '->', repr(value))
fp2.close()

# Step 4: Read the file with correct encoding (utf_8)
fp3 = open('cafe.txt', encoding='utf_8')
expression = "fp3"
value = fp3
print(expression.rjust(30), '->', repr(value))
expression = "fp3.read()"
value = fp3.read()
print(expression.rjust(30), '->', repr(value))
fp3.close()

# Step 5: Read the file in binary mode
fp4 = open('cafe.txt', 'rb')
expression = "fp4"
value = fp4
print(expression.rjust(30), '->', repr(value))
expression = "fp4.read()"
value = fp4.read()
print(expression.rjust(30), '->', repr(value))
fp4.close()

```
