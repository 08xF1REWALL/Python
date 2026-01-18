# Boofuzz
1. s.string to denote that string data contained within the primative is a fuzzable string. 
to fuzz a string, you would use s.string("test@text.com")
2. Delimiters small strings that help break larger strings into manageable pieces.
```py
s_string("justin")
s_delim("@")
s_string("example.com")
s_delim(".", fuzzable=False) # the dot in this case is not fuzzable
s_string("com")
```
3. Static and Random Primitives
pass in strings that will either be unchanging or mutated with random data. 
```py
s_static("Hello World!") 
s_static("\x41\x42\x43\x44") 
```
4. To generate random data of varying lengths, you can use s_random
```py
s_random("Justin", min_length=1, max_length=256, num_mutations=10)
```
5. Binary Data
Data representation. You can copy and paste any binary data into it and have boofuzz recognize it and fuzz it for you.
```py
s_binary("0x00 \\x41\\x42\\x43 0d 0a 0d 0a")
```
6. Integers
You can define integers of varying sizes and endianness.
1 byte – s_byte(), s_char()
2 bytes – s_word(), s_short()
4 bytes – s_dword(), s_long(), s_int()
8 bytes – s_qword(), s_double()

```py
s_word(0x1234, endian=">", fuzzable=True)  # set 2-byte word value to 0x1234, flip its endianness, and leave it as a static value.

s_dword(0xDEADBEEF, format="ascii", signed=True)  # set 4-bytes DWORD(double word) value to 0xDEADBEEF, format it as ASCII characters, and treat it as a signed .
```
7. Blocks and Groups
Blocks and groups allow you to create more complex structures by combining multiple primitives together.

blocks are a means to take sets of individual primitives and nest them into a single organized unit.

Groups are a way to chain a particular set of primatives to a block so that each primative can be cycled through on each fuzzing iteration for the particular group.
```py
from boofuzz import *

s_initialize("HTTP BASIC")

s_group("verbs", values=["GET", "POST", "TRACE"])

s_block_start("body", group="verbs")
s_delim(" ")
s_string("/")
s_delim("index.html")
s_string("HTTP")
s_delim("/")
s_string("1")
s_delim(".")
s_string("1")

# end the request with mandatory static sequences
s_static("\r\n\r\n")
s_block_end("body")
```

We see that the TippingPoint fellas have defined a group named verbs
that has all of the common HTTP request types in it. Then they defined a
block called body, which is tied to the verbs group. This means that for each
verb (GET, HEAD, POST, TRACE), Boofuzz will iterate through all mutations of the
body block. Thus Boofuzz produces a very thorough set of malformed HTTP
requests involving all the primary HTTP request types.

Boofuzz features data encoding, checksum calculators, automatic data resizers, and more. For more information, check out the Boofuzz documentation at https://boofuzz.readthedocs.io/en/latest/index.html

## 