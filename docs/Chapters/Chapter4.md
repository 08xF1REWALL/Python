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

## Unicoded Data normalize 

```py
from unicodedata import normalize
def nfc_equal(str1, str2):
    return normalize('NFC', str1) == normalize('NFC', str2)

def fold_equal(str1, str2)
    return (normalize('NFC', str1).casefold() == normalize('NFC', str2).casefold())

s1 = 'é'               # composed character: U+00E9
s2 = 'e\u0301' 
print("NFC Equal:", nfc_equal(s1, s2))
print("Fold equal:", fold_equal('straße', 'strasse'))
```

## Extreme normalization: taking out Diacritics

```py
import unicodedata
import string

def shave_marks(txt):
"""Remove all diacritic marks"""
norm_txt = unicodedata.normalize('NFD', txt) # convert the input into decomosed for using normalization form D
shaved = ''.join(c for c in norm_txt if not unicodedata.combining(print(c)) # if not unicodedata this will return 0, but for é will return  join kept thee characters into one string without any separator
return unicodedata.normalize('NFC', shaved)
text_with_accents = "café naïve élève São Tomé"
print ("original:", text_with_accent)
print ("shaved :", shave_marks(text_with_accents))
```

```py
import unicodedata
import string

def shaved_marks_latin(txt)
norm_txt = unicodedata.normalize('NFD', txt)
latin_base = False
keepers = []
for c in norm_txt:
    if unicodedata.compining(c) and latin_base:
        continue
    keepers.append(c)
    if not unicodedata.compining(c):
        latin_base = c in string.ascii_letters
    shaved = ''.join(keepers)
    return unicodedata.normalize('NFC', shaved)

text_with_accents = "café naïve élève São Tomé"
print("original:", text_with_accents)
print("shaved:", shaved_marks_latin(text_with_accents))

```

```py
# mapping table for char to char replacement
single_map = str.maketrans("""‚ƒ„†ˆ‹‘’“”•–—˜›""",
                           """'f"*^<''""---~>""")

# mapping table for char to string replacement
multi_map = str.maketrans({
 '€': '<euro>',
 '…': '...',
 'Œ': 'OE',
 '™': '(TM)',
 'œ': 'oe',
 '‰': '<per mille>',
 '‡': '**',
})
multi_map.update(single_map)

def dewinize(txt):
    """Replace Win1252 symbols with ASCII chars or sequences"""
    return txt.translate(multi_map)
def asciize(txt):
    no_masks = shave_marks_latin(dewinize(txt))
    no_marks = no_marks.replace('ß', 'ss')
    return unicodeddata.normalize('NFKC', no_marks)

```

## local strxfrm function as sort key

```py
import local
local.setlocale(locale.LC_COLLATE, 'pt_BR.UTF-8')
fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
sorted_fruits = sorted(fruites, key=local.strxfrm)
print(sorted_fruits)
```

## Using pyuca.collator.sort_key method

```py
import pyuca
coll = pyuca.Collator()
fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
sorted_fruits = sorted(fruits, key=coll.sort_key)
print(sorted_fruits)
```

## Unicode database numerical character metadata

- Unicode: is a universal standard of encoding, representating and handling text characters from virtually every language and writing system in the world.
U+0041 for 'A'

- Metadata: refers to the information about the charactes such as:

1. names (Unicode)
2. category(letter, number, punctuation)
3. digit uppercase, or printable.
4. and the numeric value.

```py
import unicodedata
import re
re_digit = re.compile(r'\d')
sample = '1\xbc\xb2\u0969\u136b\u216b\u2466\u2480\u3285'
for char in sample : 
    char.center(6),
    're_dig' if re_digit.match(char) else '-',
    'isdig' if char.isdigit() else '-',
    'isnum' if char.isnumeric() else '-',
    format(unicodedata.numeric(char), '5.2f'),
    unicodedata.name(char),
    sep='\t')
```