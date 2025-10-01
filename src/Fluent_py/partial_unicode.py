import unicodedata, functools
nfc = functools.partial(unicodedata.normalize, ('NFC'))
s1 = 'cafè'
s2 = 'cafe\u0301'
print(s1, s2)
print(s1 == s2)
print(nfc(s1) == nfc(s2))
