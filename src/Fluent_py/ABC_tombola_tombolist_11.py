from random import randrange
from main.ABC_tombola_11 import Tombola

@Tombola.register # Tombolist is registered as a virtual subclass of Tombola.
class TomboList(list):
    def pick(self):
        if self:
            position = randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pop from empty TomboList')
        
    load = list.extend
    
    def loaded(self):
        return bool(self)
    
    def inspect(self):
        return tuple(sorted(self))
    