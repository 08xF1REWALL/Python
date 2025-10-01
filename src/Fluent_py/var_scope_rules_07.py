from dis import dis
def f1(a):
    print(a)
    print(b)
    b = 6


def f2(a):
    print(a)
    print(b)
b = 8
"""
def f3(a):
    global b
    print(a)
    print(b)
    b = 9
"""

#f1(3)
#f2(2)
#f3(4)
print(dis(f1))
print(dis(f2))
