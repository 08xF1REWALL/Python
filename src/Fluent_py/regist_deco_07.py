registey = [] # will hold reference to func decorated by @register
def register(func):
    print('running register(%s)' % func)
    registey.append(func)
    return func

@register
def f1():
    print('running f()')

@register
def f2():
    print('running f2()')

def f3():
    print('running f()')

def main():
    print('running main()')
    print('registry ->', registey)
    f1()
    f2()
    f3()

if __name__=='__main__':
    main()