import time
import weakref
a_set = {0, 1}              # Strong reference: a_set points to {0, 1}
wref = weakref.ref(a_set)   # Weak reference: wref points to the same {0, 1}
print(wref)                 # <weakref at 0x100637598; to 'set' at 0x100636748>
print(wref())               # {0, 1}
a_set = {2, 3, 4}           # Rebind a_set to a new set, removing strong reference to {0, 1}, in this case this will be no longer strong ref, and make it eligble for garbage collection. 
print(wref())               # {0, 1}
time.sleep(1)
print(wref() is None)       # False
time.sleep(1)
print(wref() is None)       # True