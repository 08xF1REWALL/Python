cafe = bytes('Café', encoding='utf_8')
print(cafe)
print(cafe[0]) # ASCII -> hex -> decimal
print(cafe[:1]) # gives a slice of the first byte as bytes object "b'c'"
cafe_arr = bytearray(cafe) # mutable version of byte
print(cafe_arr)
print(cafe_arr[-1:]) # gives a slice of the last byte of the bytearray

