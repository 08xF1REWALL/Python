from abc import ABC, abstractmethod
from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')

class LineItem:
    def __init__(self, product,quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price
        
    def total(self):
        return self.price * self.quantity
    
class Order:
    
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion
        
    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total
        
    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion(self)
        return self.total() - discount
        
    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())
    
        
def fidelity_promo(order):  # Kleinschreibung für Funktionsnamen
    """5% discount for customer with 1000 or more fidelity points"""
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0

def bulk_item_promo(order):  # Kleinschreibung für Funktionsnamen
    """"10% discount for each LineItem with 20 or more units"""
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount
    
def large_order_promo(order):  # Kleinschreibung für Funktionsnamen
    """7% discount for orders with 10 or more distinct item"""
    distinct_item = {item.product for item in order.cart}
    if len(distinct_item) >= 10:
        return order.total() * .07
    return 0

# Liste aller verfügbaren Rabattfunktionen
promos = [fidelity_promo, bulk_item_promo, large_order_promo]

def best_promo(order):
    """Select best discount available"""
    return max(promo(order) for promo in promos)

if __name__ == '__main__':
    # Testbeispiele
    joe = Customer('John Doe', 0)
    ann = Customer('Ann Smith', 1100)
    
    # Normaler Warenkorb
    cart = [LineItem('banana', 4, .5),
            LineItem('apple', 10, 1.5),
            LineItem('watermellon', 5, 5.0)]
            
    # Test verschiedener Rabatte
    print('Normaler Warenkorb mit verschiedenen Rabatten:')
    print(f'Kein Rabatt: {Order(joe, cart)}')
    print(f'Treuerabatt (Joe): {Order(joe, cart, fidelity_promo)}')
    print(f'Treuerabatt (Ann): {Order(ann, cart, fidelity_promo)}')
    
    # Warenkorb für Mengenrabatt
    banana_cart = [LineItem('banana', 30, .5),
                  LineItem('apple', 10, 1.5)]
    print('\nWarenkorb mit vielen Bananen:')
    print(f'Mengenrabatt: {Order(joe, banana_cart, bulk_item_promo)}')
    
    # Warenkorb für Großbestellung
    long_cart = [LineItem(str(item_code), 1, 1.0)
                for item_code in range(10)]
    print('\nWarenkorb mit vielen verschiedenen Artikeln:')
    print(f'Großbestellungsrabatt: {Order(joe, long_cart, large_order_promo)}')
    
    # Test des besten Rabatts
    print('\nBester Rabatt für verschiedene Warenkörbe:')
    print(f'Bester Rabatt (normaler Warenkorb): {Order(ann, cart, best_promo)}')
    print(f'Bester Rabatt (Mengenrabatt): {Order(joe, banana_cart, best_promo)}')
    print(f'Bester Rabatt (Großbestellung): {Order(joe, long_cart, best_promo)}')
