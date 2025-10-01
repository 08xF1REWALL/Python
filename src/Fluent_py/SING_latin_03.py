from unicodedata import name
result = {chr(i) for i in range(0x110000) if 'SING' in name(chr(i), '')}
print(result)