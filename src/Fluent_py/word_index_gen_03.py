import re # regular expression
import sys # system-specific parameters and functions
import os # operating system dependent functionality
#DIAL_CODES = [(86, 'China'), (91, 'India'), (1, 'United States'), (62, 'Indonesia'), (55, 'Brazil'), (92, 'Pakistan'), (880, 'Bangladesh'), (234, 'Nigeria'), (7, 'Russia'), (81, 'Japan')]
WORD_RE = re.compile(r'\w+')
index = {}

#for line_no, (_, country) in enumerate(DIAL_CODES, 1):
with open(sys.argv[1], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group() # gives the matched word
            column_no = match.start() # gives the starting position or the index
            location = (line_no, column_no) # tuple of line number and column number
            #print(word, location) # for debugging
            occurrences = index.get(word, []) 
            occurrences.append(location) # 
            index[word] = occurrences

for word in sorted(index, key=str.upper):
    print(word, index[word])