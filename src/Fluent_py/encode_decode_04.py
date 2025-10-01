a = 'café'
print(len(a))       # 4 characters
b = a.encode('utf8')
print(b)            # b'caf\xc3\xa9'
print(len(b))       # 5 bytes

