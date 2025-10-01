import struct
#from tkinter import image_types

def parse_gif_header(filepath):
    with open('/mnt/c/Users/berne/Desktop/Books_to_learn-main/Books_to_learn-main/Python/tests/unit/filter.gif', 'rb') as f:
        gif_bytes = f.read()
    #print(gif_bytes)
    print("\nHex representation:")
    print(gif_bytes.hex())
    print("Header", gif_bytes[:6])

    # Read the first 13 bytes: Header + Logical Screen Descriptor
    header = gif_bytes[:13]
    sig, ver, width, height, packed, bg_color, aspect_ratio = struct.unpack('<3s3sHHBBB', header)

    print("=== GIF Header Information ===")
    print("Signature:", sig.decode())
    print("Version:", ver.decode())
    print("Width:", width)
    print("Height:", height)
    print("Packed Field (byte 10):", f'{packed:08b}')
    print("  Global Color Table Flag:", (packed >> 7) & 1)
    print("  Color Resolution:", ((packed >> 4) & 0b111) + 1)
    print("  Sort Flag:", (packed >> 3) & 1)
    print("  Global Color Table Size:", 2 ** ((packed & 0b111) + 1))
    print("Background Color Index:", bg_color)
    print("Pixel Aspect Ratio:", aspect_ratio)

    print("\n=== Raw Bytes (First 20 Bytes) ===")
    print(' '.join(f'{b:02x}' for b in gif_bytes[:20]))

if __name__ == '__main__':
    # Change the path as needed
    parse_gif_header('filter.gif')
    #parse_gif_header('/mnt/c/Users/berne/Desktop/Books_to_learn-main/Books_to_learn-main/Python/tests/unit/filter.gif')
    