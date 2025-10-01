import unicodedata
import re

re_digit = re.compile(r'\d')
sample = '1\xbc\xb2\u0969\u136b\u216b\u2466\u2480\u3285'

for char in sample:
    print(
        'U+%04X' % ord(char),               # Unicode code point ord char to int %04X to uppercase hexadecimal, 04 pads it with zeros to 4 digits.
        char.center(6),                     # Character itself, padded, return a string of length 6 with the character, and it add spaces to the right and the left.
        're_dig' if re_digit.match(char) else '-',   # Regex \d match
        'isdig' if char.isdigit() else '-',          # isdigit()
        'isnum' if char.isnumeric() else '-',        # isnumeric()
        format(unicodedata.numeric(char), '5.2f'),   # Numeric value
        unicodedata.name(char),                      # Unicode name
        sep='\t'
    )

