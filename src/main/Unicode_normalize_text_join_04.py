import unicodedata
import string

def shave_marks(txt):
    """Remove all diacritic marks"""
    norm_txt = unicodedata.normalize('NFD', txt) # convert the input into decomosed for using normalization form D
    shaved_chars = []
    for c in norm_txt:
        print(f"Character: {repr(c)} | Name: {unicodedata.name(c, 'UNKNOWN')} | Compining: {unicodedata.combining(c)}")
        if not unicodedata.combining(c):
            shaved_chars.append
    
    shaved = ''.join(shaved_chars) # if not unicodedata this will return 0, but for é will return  join kept thee characters into one string without any separator
    return unicodedata.normalize('NFC', shaved)
# Example
text_with_accents = "café naïve élève São Tomé"
print("Original:", text_with_accents)
print ("shaved :", shave_marks(text_with_accents))