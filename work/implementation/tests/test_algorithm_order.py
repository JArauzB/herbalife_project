import unittest
import csv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from implementation.algorithm import Order
from implementation.algorithm import Product

# IMPORT FILE USING REFLECTION
current_dir = os.path.dirname(os.path.abspath(__file__))

class TestOrder(unittest.TestCase):
    """
    Test the Order class.
    
    The Order class represents an order with a list of items.
    
    Methods:
        setUp: Initializes the test case.
        test_add_item: Test that the add_item method adds an item to the order.
        test_add_items: Test that the add_items method adds a list of items to the order.
        test_add_rejected_item: Test that the add_rejected_item method adds an item to the list of rejected items.
        test_reset_rejected_items: Test that the reset_rejected_items method resets the list of rejected items.
        test_reset_all_items: Test that the reset_all_items method resets the list of taken items and rejected items.
        test_order_items: Test that the order_items method sorts the items in the order by volume, then by dimensions, then by weight.
        test_get_items: Test that the get_items method returns the list of items in the order.
        test_take_item: Test that the take_item method removes the first item from the order.
        test_take_specific_item: Test that the take_specific_item method removes the specified item from the order.
        test_get_order_number: Test that the get_order_number method returns the order number.
        test_take_item_empty: Test that the take_item method returns None if the order is empty.
        test_take_specific_item_not_in_order: Test that the take_specific_item method returns None if the item is not in the order.
        test_get_total_volume: Test that the total volume of the order is the sum of the volumes of the products in the order.
        test_get_total_weight: Test that the total weight of the order is the sum of the weights of the products in the order.
        test_get_dimensions: Test that the dimensions of the order are the maximum dimensions of the products in the order.
    """

    def setUp(self):
        """
        Initializes the Order object with the specified order number and date and time.
        """
        self.products = []

        with open(os.path.join(current_dir, './test_files/product_definitions.csv'), mode='r') as file:
            reader = csv.DictReader(file)
            products = list(reader)

            for product in products:
                self.products.append(
                    Product(
                        width=float(product['Width']),
                        height=float(product['Height']),
                        length=float(product['Length']),
                        weight=float(product['Weight']),
                        fit_ratio=float(product['Fit ratio']),
                        item=product['ID'],
                        location=product['Location']
                    )
                )

        sublist = self.products[0:2]

        self.order = Order(1, "2023-10-01", sublist)

    def test_add_item(self):
        """
        Test that the add_item method adds an item to the order.
        """
        self.order.add_item(self.products[3])
        self.assertIn(self.products[3], self.order.items)

    def test_add_items(self):
        """
        Test that the add_items method adds a list of items to the order.
        """
        subset = self.products[2:]
        self.order.add_items(subset)
        self.assertIn(self.products[3], self.order.items)

    def test_add_rejected_item(self):
        """
        Test that the add_rejected_item method adds an item to the list of rejected items.
        """
        self.order.add_rejected_item(self.products[3])
        self.assertIn(self.products[3], self.order.rejected_items)

    def test_reset_rejected_items(self):
        """
        Test that the reset_rejected_items method resets the list of rejected items.
        """
        self.order.add_rejected_item(self.products[3])
        self.order.reset_rejected_items()
        self.assertIn(self.products[3], self.order.items)
        self.assertEqual(len(self.order.rejected_items), 0)

    def test_reset_all_items(self):
        """
        Test that the reset_all_items method resets the list of taken items and rejected items.
        """
        self.order.add_rejected_item(self.products[3])
        self.order.take_specific_item(self.products[3])
        self.order.reset_all_items()
        self.assertIn(self.products[3], self.order.items)
        self.assertIn(self.products[0], self.order.items)
        self.assertEqual(len(self.order.rejected_items), 0)
        self.assertEqual(len(self.order.taken_items), 0)

    def test_order_items(self):
        """
        Test that the order_items method sorts the items in the order by volume, then by dimensions, then by weight.
        """
        subset = self.products[2:]
        self.order.add_items(subset)
        self.order.order_items()
        self.assertEqual(self.order.items[0], self.products[2])

    def test_get_items(self):
        """
        Test that the get_items method returns the list of items in the order.
        """
        items = self.order.get_items()
        self.assertEqual(items, [self.products[0], self.products[1]])

    def test_take_item(self):
        """
        Test that the take_item method removes the first item from the order.
        """
        item = self.order.take_item()
        self.assertEqual(item, self.products[0])
        self.assertNotIn(item, self.order.items)

    def test_take_specific_item(self):
        """
        Test that the take_specific_item method removes the specified item from the order.
        """
        self.order.take_specific_item(self.products[1])
        self.assertNotIn(self.products[1], self.order.items)

    def test_get_order_number(self):
        """
        Test that the get_order_number method returns the order number.
        """
        order_number = self.order.get_order_number()
        self.assertEqual(order_number, 1)

    def test_take_item_empty(self):
        """
        Test that the take_item method returns None if the order is empty.
        """
        item = self.order.take_item()
        self.assertIsNotNone(item)

        item = self.order.take_item()
        self.assertIsNotNone(item)
        
        item = self.order.take_item()
        self.assertIsNone(item)

    def test_take_specific_item_not_in_order(self):
        """
        Test that the take_specific_item method returns None if the item is not in the order.
        """
        new_product = Product(width=10, height=10, length=10, weight=10, fit_ratio=99, item='999', location=1)
        taken_product = self.order.take_specific_item(new_product)
        self.assertEqual(taken_product, None)
        
        remaining_products = self.order.get_items()
        self.assertNotIn(new_product, remaining_products)
    
    def test_get_total_volume(self):
        """
        Test that the total volume of the order is the sum of the volumes of the products in the order.
        """
        total_volume = self.order.get_total_volume()
        expected_volume = sum([item.volume() for item in self.order.items])
        self.assertEqual(total_volume, expected_volume)

    def test_get_total_weight(self):
        """
        Test that the total weight of the order is the sum of the weights of the products in the order.
        """
        total_weight = self.order.get_total_weight()
        expected_weight = sum([item.weight for item in self.order.items])
        self.assertEqual(total_weight, expected_weight)

    def test_get_dimensions(self):
        """
        Test that the dimensions of the order are the maximum dimensions of the products in the order.
        
        The dimensions of the order are the maximum dimensions of the products in the order.
        """
        dimensions = self.order.get_dimensions()
        sorted_dimensions = sorted(
            [(item.width, item.height, item.length) for item in self.order.items],
            key=lambda dims: sorted(dims, reverse=True),
            reverse=True
        )
        expected_dimensions = [
            max([dims[0] for dims in sorted_dimensions]),
            max([dims[1] for dims in sorted_dimensions]),
            max([dims[2] for dims in sorted_dimensions])
        ]
        self.assertEqual(dimensions, expected_dimensions)

    def test_add_rejected_item_removes_from_items(self):
        """
        Test that the add_rejected_item method removes the item from the items list if it exists.
        """
        self.order.add_item(self.products[3])
        self.assertIn(self.products[3], self.order.items)
        self.order.add_rejected_item(self.products[3])
        self.assertNotIn(self.products[3], self.order.items)

    def test_add_rejected_item_removes_from_taken_items(self):
        """
        Test that the add_rejected_item method removes the item from the taken items list if it exists.
        """
        self.order.add_item(self.products[3])
        taken_item = self.order.take_item()
        self.assertIn(taken_item, self.order.taken_items)
        self.order.add_rejected_item(taken_item)
        self.assertNotIn(taken_item, self.order.taken_items)