import unicodedata
import string

def shave_marks_latin(txt):
    norm_txt = unicodedata.normalize('NFD', txt)
    latin_base = False
    keepers = []
    for c in norm_txt:
        if unicodedata.combining(c) and latin_base:
            continue
        keepers.append(c)
        if not unicodedata.combining(c):
            latin_base = c in string.ascii_letters
    shaved = ''.join(keepers)
    return unicodedata.normalize('NFC', shaved)

text_with_accents = "café naïve élève São Tomé"
print("original:", text_with_accents)
print("shaved:", shave_marks_latin(text_with_accents))