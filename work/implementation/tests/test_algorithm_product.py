import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from implementation.algorithm import Product

class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product1 = Product(10, 20, 30, 500, 100, "Product1", 1)
        self.product2 = Product(15, 25, 35, 600, 100, "Product2", 1)
        self.product3 = Product(10, 20, 30, 500, 100, "Product3", 2)
        self.product4 = Product(10, 20, 30, 400, 100, "Product4", 5)
        self.product5 = Product(5, 10, 15, 500, 100, "Product5", 5)
        self.product6 = Product(10, 20, 30, 500, 99, "Product6", 6) # 10 * 20 * 30 = 6000 (fit ratio is 99% for this product, so the volume is 5940)

    def test_volume(self):
        self.assertEqual(self.product1.volume(), 6000)              # 10 * 20 * 30
        self.assertEqual(self.product2.volume(), 13125)             # 15 * 25 * 35
        self.assertEqual(self.product3.volume(), 6000)              # 10 * 20 * 30

    def test_compare(self):
        self.assertEqual(self.product1.__lt__(self.product2), True)  # Compare by volume
        self.assertEqual(self.product2.__lt__(self.product1), False)   # Compare by volume
        self.assertEqual(self.product1.__lt__(self.product6), False)   # Compare by volume, but with fit ratio
        self.assertEqual(self.product1.__lt__(self.product3), False)   # Equal products

    def test_compare_by_dimensions(self):
        self.assertEqual(self.product1.__lt__(self.product5), False)   # Compare by dimensions
        self.assertEqual(self.product5.__lt__(self.product1), True)  # Compare by dimensions

    def test_compare_by_weight(self):
        self.assertEqual(self.product1.__lt__(self.product4), False)   # Compare by weight
        self.assertEqual(self.product4.__lt__(self.product1), True)  # Compare by weight

    def test_compare_equal_volume_inequal_dimensions(self):
        product7 = Product(10, 10, 10, 500, 100, "Product7", 1)
        product8 = Product(100, 1, 10, 500, 100, "Product8", 1)

        self.assertEqual(product7.__lt__(product8), True)  # Compare by individual dimensions
