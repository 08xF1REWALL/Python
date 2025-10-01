import bisect
import sys

def grade(score, breakpoints, grades):
    i = bisect.bisect(breakpoints, score)
    return grades[i]
breakpoints = [60, 70, 80, 90]
grades = ['F', 'D', 'C', 'B', 'A']

scores = [33, 55, 77, 88, 99]

result = [grade(score, breakpoints, grades) for score in scores]
print(result)  # Output: ['F', 'F', 'C', 'B', 'A'] 



