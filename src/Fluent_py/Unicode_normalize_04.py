from unicodedata import normalize

def nfc_equal(str1, str2):
    return normalize('NFC', str1) == normalize('NFC', str2)

def fold_equal(str1, str2):
    return normalize('NFC', str1).casefold() == normalize('NFC', str2).casefold()

# Examples
s1 = 'é'               # composed character: U+00E9
s2 = 'e\u0301'         # decomposed: 'e' + combining acute accent

print("NFC Equal:", nfc_equal(s1, s2))       # True, after NFC normalization
print("Fold Equal:", fold_equal('Straße', 'strasse'))  # True, after casefold
