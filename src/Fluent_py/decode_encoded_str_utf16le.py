byte_seq = b'\xff\xfeE\x00l\x00 \x00N\x00i\x00\xf1\x00o\x00'

decode_str = byte_seq.decode('utf_16')
print(f"Decoded string: {decode_str}")