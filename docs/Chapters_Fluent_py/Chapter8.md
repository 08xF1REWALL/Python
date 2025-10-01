# Object-Oriented Idioms
## The Relative Immutable of tubles 
in this case we have a tuble that contains a list which is modifyable
```py
t1 = (1, 2, [30, 40])
t2 = (1, 2, [30, 40])
print(t1 == t2)  # True
print(id(t1[-1]))  # e.g., 4302515784
t1[-1].append(99)
print(t1)  # (1, 2, [30, 40, 99])
print(id(t1[-1]))  # e.g., 4302515784
print(t1 == t2)  # False
```

```py
l1 = [3, [55, 44], (7, 8, 9)]
l2 = list(l1)
print(l2)
print(l2 == l1) #-> true
print(l2 is l1) #-> false referece to different obj


```

```py
l1 = [3, [66, 55, 44], (7, 8, 9)]
l2 = list(l1)
l1.append(100)
l1[1].remove(55)
print('l1:', l1)
print('l2:', l2)
l2[1] += [33, 22]
l2[2] += [10, 11]
print('l1:', l1)
print('l2:', l2)

```
check picture for futher understanding of the call by object reference

## Deep and Shallow Copies of Arbitrary Objects

```py
import copy

class Bus:
    def __init__(self, passengers=None):
        if passengers is None:
            self.passangers =[]
        else:
            self.passangers = list(passengers)
    
    def pick(self, name):
        self.passangers.append(name)
    
    def drop(self, name):
        self.passangers.remove(name)
bus1 = Bus(['Alice', 'Bill', 'Claire', 'David'])
bus2 = copy.copy(bus1)
bus3 = copy.deepcopy(bus1)
print(id(bus1), id(bus2), id(bus3))
bus1.drop('Bill')
print(bus1.passangers, bus2.passangers)
print(bus3.passangers)
print(id(bus1), id(bus2), id(bus3))
print(id(bus1.passangers), id(bus2.passangers), id(bus3.passangers))

```

## Function Parameters as References 

```py
class HauntedBus:
 """A bus model haunted by ghost passengers"""
    def __ini__(self, passangers[]):
        self.passengers = passengers
    def pick(self, name):
        self.passengers.append(name)

    def drop(self, name):
        self.passengers.remove(name)

bus1 = HauntedBus(['Alice', 'Bill'])
print(bus1.passengers)
bus1.pick('Charlie')
bus1.drop('Alice')
print(bus1.passengers)
bus2 = HauntedBus()
bus1.pick('Carrie')
print(bus2.passengers)
print(dir(HautedBus.__init__))
print(HauntedBus.__init__.__defaults__)
print(HauntedBus.__init__.__defaults__[0] is bus2.passangers)


```

# del and Garbage Collection

```py
import weakref
s1 = {1, 2, 3}
s2 = s1
def bye():
    print('Gone with the wind ...')

ender = weakref.finalize(s1, bye)
print(ender.alive)
del s1
#print(s1)
s2 = 'spam'
print(ender.alive)
print(ender.alive)

```
- after deleting the s1 the reference between it and s2 was removed there for we get flase, this happens after assigning the s2 variable new value.

## Weak References

```py
import weakref
a_set = {0, 1}              # Strong reference: a_set points to {0, 1}
wref = weakref.ref(a_set)   # Weak reference: wref points to the same {0, 1}
print(wref)                 # <weakref at 0x100637598; to 'set' at 0x100636748>
print(wref())               # {0, 1}
a_set = {2, 3, 4}           # Rebind a_set to a new set, removing strong reference to {0, 1}, in this case this will be no longer strong ref, and make it eligble for garbage collection. 
print(wref())               # {0, 1}
print(wref() is None)       # False
print(wref() is None)       # True
```

## The WeakValueDictionary Skit

```py
impor

```