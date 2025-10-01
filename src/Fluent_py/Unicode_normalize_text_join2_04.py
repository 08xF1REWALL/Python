import unicodedata
def shave_marks(txt):
    """Remove all diacritic marks (accents) from a string."""
    norm_txt = unicodedata.normalize('NFD', txt)
    shaved_chars = []
    combining_valus = []
    
    for c in norm_txt:
        combining_valus.append(unicodedata.combining(c))
        if not unicodedata.combining(c):
            shaved_chars.append(c)
    shaved = ''.join(shaved_chars)
    print("Combining values:", combining_valus)
    return unicodedata.normalize('NFC', shaved)

# Example usage
text_with_accents = "café naïve élève São Tomé"
print("Original:", text_with_accents)
print("Shaved  :", shave_marks(text_with_accents))