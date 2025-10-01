import unittest
from discount_strategie_func_call_06 import (
    Customer, LineItem, Order,
    FidelityPromo, BulkItemPromo, LargeOrderPromo
)

class TestDiscountStrategies(unittest.TestCase):
    def setUp(self):
        # Testdaten vorbereiten
        self.joe = Customer('John Doe', 0)
        self.ann = Customer('Ann Smith', 1100)
        self.basic_cart = [
            LineItem('banana', 4, 0.5),
            LineItem('apple', 10, 1.5),
            LineItem('watermelon', 5, 5.0)
        ]
        self.bulk_cart = [
            LineItem('banana', 30, 0.5),  # Qualifiziert für Mengenrabatt
            LineItem('apple', 10, 1.5)
        ]
        self.large_cart = [
            LineItem('item1', 1, 1.0),
            LineItem('item2', 1, 1.0),
            LineItem('item3', 1, 1.0),
            LineItem('item4', 1, 1.0),
            LineItem('item5', 1, 1.0),
            LineItem('item6', 1, 1.0),
            LineItem('item7', 1, 1.0),
            LineItem('item8', 1, 1.0),
            LineItem('item9', 1, 1.0),
            LineItem('item10', 1, 1.0),
        ]

    def test_order_total(self):
        """Test der Gesamtsummenberechnung ohne Rabatt"""
        order = Order(self.joe, self.basic_cart)
        expected = 4 * 0.5 + 10 * 1.5 + 5 * 5.0  # 2 + 15 + 25 = 42
        self.assertEqual(order.total(), 42.0)

    def test_fidelity_promo_no_discount(self):
        """Test des Treuerabatts für Kunden ohne ausreichende Punkte"""
        order = Order(self.joe, self.basic_cart, FidelityPromo)
        self.assertEqual(order.due(), 42.0)  # Kein Rabatt

    def test_fidelity_promo_with_discount(self):
        """Test des Treuerabatts für Kunden mit ausreichenden Punkten"""
        order = Order(self.ann, self.basic_cart, FidelityPromo)
        expected = 42.0 * 0.95  # 5% Rabatt
        self.assertAlmostEqual(order.due(), expected, places=2)

    def test_bulk_item_promo(self):
        """Test des Mengenrabatts"""
        order = Order(self.joe, self.bulk_cart, BulkItemPromo)
        # 30 Bananen für 0.5 = 15.0 (10% Rabatt = 1.5)
        # 10 Äpfel für 1.5 = 15.0 (kein Rabatt)
        # Gesamt: 30.0 - 1.5 = 28.5
        self.assertEqual(order.due(), 28.5)

    def test_large_order_promo(self):
        """Test des Großbestellungsrabatts"""
        order = Order(self.joe, self.large_cart, LargeOrderPromo)
        # 10 Artikel für je 1.0 = 10.0
        # 7% Rabatt auf die Gesamtsumme
        expected = 10.0 * 0.93
        self.assertAlmostEqual(order.due(), expected, places=2)

    def test_no_promotion(self):
        """Test ohne Rabattaktion"""
        order = Order(self.joe, self.basic_cart)
        self.assertEqual(order.due(), order.total())

if __name__ == '__main__':
    unittest.main()
