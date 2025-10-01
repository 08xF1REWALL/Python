arabic_text = 'مرحبا بكم يا حلوين'

for codec in ['utf_8', 'utf_16', 'utf_16_be', 'iso8859_6']:
    encodeed = arabic_text.encode(codec)
    print(f"{codec}:\t {encodeed}")