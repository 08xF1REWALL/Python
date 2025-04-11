from array import array

numbers = array('h', [-2, -1, 0, 1, 2])
memv = memoryview(numbers)
print(len(memv))
print(memv[0])
memv_oct = memv.cast('B')

# Get decimal values of the bytes
decimal_values = memv_oct.tolist()
print("Decimal values of bytes:", decimal_values)

# Convert each byte to binary (8 bits)
binary_values = [format(byte, '08b') for byte in decimal_values]
print("Binary values of bytes:", ' '.join(binary_values))

memv_oct[5] = 4
# [254, 255, 255, 255, 0, 4, 1, 0, 2, 0] 
# calculated as: low byte first high byte second Value=(high byte * 256) + low byte
# value = 4 * 256 + 0 = 1024 in binary 000000100 0000000
decimal_values_after = memv_oct.tolist()
binary_values_after = [format(byte, '08b') for byte in decimal_values_after]
print("\nAfter modification (memv_oct[5] = 4):")
print("Numbers:", numbers)
print("Decimal values of bytes:", decimal_values_after)

print(numbers, decimal_values)
print(memv_oct.tolist())

# Get decimal values of the bytes after modification
