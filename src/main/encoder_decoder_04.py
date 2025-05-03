import numpy as np

city = ['München', 'Düsseldorf', 'Köln', 'Göttingen', 'Münster']

# Loop through different encodings and print bytes representations
for codec in ['latin_1', 'utf_8', 'utf_16', 'iso8859_1']:
    print(f"\nEncoding: {codec}")
    for citys in city:
        print(citys, citys.encode(codec), sep='\t')  # Print each city's bytes
    print(codec, 'Düsseldorf'.encode(codec), sep='\t')

# Print lists of encoded bytes for each encoding
print('\nEncoding individual cities:')
print('utf_8', [c.encode('utf_8') for c in city], sep='\t')
print('utf_16', [c.encode('utf_16') for c in city], sep='\t')
print('utf_16_be', [c.encode('utf_16_be') for c in city], sep='\t')
print('iso8859_1', [c.encode('iso8859_1') for c in city], sep='\t')

# Create a NumPy array of utf_8-encoded bytes objects for all cities
bytes_list = [citys.encode('utf_16') for citys in city]
np_bytes = np.array(bytes_list, dtype=object)  # Use dtype=object for variable-length bytes
print('\nNumPy array of utf_8-encoded bytes objects:')
print(np_bytes)

# Create and print NumPy arrays of byte values for each city
print('\nNumPy arrays from bytes for each city (utf_8):')
for citys in city:
    b = citys.encode('utf_8')  # Encode each city to bytes
    np_city = np.frombuffer(b, dtype=np.uint8)  # Create NumPy array of byte values
    print(f"{citys}: {np_city}")