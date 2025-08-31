import random
from main.ABC_tombola_11 import Tombola

class BingoCage(Tombola):
    def __init__(self, item):
        self._randomizer = random.SystemRandom()
        self._items = []
        self.load(item)

    def load(self, items):
        self._items.extend(items)
        self._randomizer.shuffle(self._items)

    def pick(self):
        try:
            return self._item.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')
    
    def call(self):
        self.pick()