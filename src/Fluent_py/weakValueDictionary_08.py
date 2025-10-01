import weakref

class Cheese:
    def __init__(self, kind):
        self.kind = kind

    def __repr__(self):
        return 'Cheese(%r)' % self.kind

stock = weakref.WeakKeyDictionary()
catalog = [Cheese('Red Leister'), Cheese('Tilsit'), Cheese('Brie'), Cheese('Parmesan')]

for cheese in catalog:
    stock[cheese.kind] = cheese

print(sorted(stock.key()))
del catalog
print(sorted(stock.key()))
del cheese
print(sorted(stock.key()))
