import os
from barcode import Code128
from barcode.writer import ImageWriter

# Sample data
devices = {
    "laptop": 3,
    "mobile": 5,
    "beamer": 2
}

# Output folder
output_dir = "barcodes"
os.makedirs(output_dir, exist_ok=True)

# Create barcodes
for category, count in devices.items():
    for i in range(1, count + 1):
        # Generate a unique code, e.g., LAPTOP001, LAPTOP002, etc.
        code = f"{category.upper()}{str(i).zfill(3)}"
        barcode = Code128(code, writer=ImageWriter())
        filename = os.path.join(output_dir, code)
        barcode.save(filename)
        print(f"Generated barcode for: {code}")
