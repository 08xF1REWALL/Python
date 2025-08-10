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