import struct

fmt = '<3s3sHH'

with open('/mnt/c/Users/berne/Desktop/Books_to_learn-main/Books_to_learn-main/Python/tests/unit/filter.gif', 'rb') as f:
    img = memoryview(f.read())
    header = img[:10] # memoryview slice of the first 10 bytes
    data = struct.unpack(fmt, header)

print("Signature:", data[0].decode())
print("Version:", data[1].decode())
print("Width:", data[2])
print("Height:", data[3])
print("Header:", header)
print("Header length:", len(header))
del header
#print("Header after deletion:", header)
#del img
