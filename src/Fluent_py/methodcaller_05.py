from operator import methodcaller
s = 'the time has come'
upcase = methodcaller('upper')
print(upcase(s))
t = methodcaller('replace', ' ', '-')
print(t(s))
print(str.upper(s))