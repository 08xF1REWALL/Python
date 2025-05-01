import struct

fmt = '<3s3sHH'

with open('/mnt/c/Users/berne/Desktop/Books_to_learn-main/Books_to_learn-main/Python/tests/unit/filter.gif', 'rb') as f:
    img = memoryview(f.read())
    header = img[:10]
    data = struct.unpack(fmt, header)

print("Signature:", data[0].decode())
print("Version:", data[1].decode())
print("Width:", data[2])
print("Height:", data[3])

