import unittest
import os
import sys
from unittest.mock import MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from implementation.algorithm import OrderManager
from implementation.algorithm import Order
from implementation.algorithm import Product

current_dir = os.path.dirname(os.path.abspath(__file__))

class TestOrderManager(unittest.TestCase):

    def setUp(self):
        self.order_manager = OrderManager(
            orderline_file_path=os.path.join(current_dir, './test_files/order_with_few_items.csv'),
            product_file_path=os.path.join(current_dir, './test_files/product_definitions.csv')
        )

    def test_load_products(self):
        products = self.order_manager.load_products()
        self.assertEqual(len(products), 5)

    def test_load_orders(self):
        orders = self.order_manager.load_orders()
        self.assertEqual(len(orders), 32)

    def test_group_by_order(self):
        orders = self.order_manager.load_orders()
        grouped_orders = self.order_manager.group_by_order(orders)
        self.assertEqual(len(grouped_orders), 5)


    def test_create_order1(self):
        orders = self.order_manager.load_orders()
        grouped_orders = self.order_manager.group_by_order(orders)
        print(f"Grouped Data Keys: {list(grouped_orders.keys())}")  # Debug

        self.assertIn('5R02891084', grouped_orders)
        print(f"Grouped Data for '5R02891084': {grouped_orders['5R02891084']}")

        total_picked = sum(int(item.get('Picked', 1)) for item in grouped_orders['5R02891084'])
        print(f"Total picked quantity for '5R02891084': {total_picked}")

        order = self.order_manager.create_order(grouped_orders['5R02891084'])
        self.assertIsInstance(order, Order)
        self.assertEqual(order.order_number, '5R02891084')

        print(f"Total items in created order: {len(order.items)}")
        for product in order.items:
            print(
                f"Product ID: {product.item}, Dimensions: {product.width}x{product.height}x{product.length}, Weight: {product.weight}")

        self.assertEqual(len(order.items), 9)  # Expected item count

    # def test_start_processing(self):
        # self.order_manager.process_orders()
        # Add assertions based on the expected behavior of start_processing

    def test_create_order_with_picked_quantity(self):
        # Mocked product data
        mocked_products_data = [
            {"ID": "Product_5252", "Width": 113, "Height": 208, "Length": 113, "Weight": 900.0, "Fit ratio": 100},
            {"ID": "Product_2037", "Width": 45, "Height": 243, "Length": 113, "Weight": 560.0, "Fit ratio": 100},
        ]

        # Mocked order data
        mocked_order_data = [
            {"Ordernr": "12345", "Date": "5-12-2024 14:00", "ID": "Product_5252", "Picked": 2, "Location": "06C01"},
            {"Ordernr": "12345", "Date": "5-12-2024 14:00", "ID": "Product_2037", "Picked": 1, "Location": "06C01"},
        ]

        # Initialize OrderManager and mock `load_products`
        order_manager = OrderManager()
        order_manager.load_products = MagicMock(return_value=mocked_products_data)

        # Call `create_order`
        created_order = order_manager.create_order(mocked_order_data)

        # Validate order number and date
        self.assertEqual(created_order.order_number, "12345")
        self.assertEqual(created_order.date_time, "5-12-2024 14:00")

        # Validate the number of items in the order
        self.assertEqual(len(created_order.items), 3)  # 2x Product_5252, 1x Product_2037

        # Validate the products in the order
        product_counts = {}
        for product in created_order.items:
            product_counts[product.item] = product_counts.get(product.item, 0) + 1

        self.assertEqual(product_counts["Product_5252"], 2)  # 2 items of Product_5252
        self.assertEqual(product_counts["Product_2037"], 1)  # 1 item of Product_2037

        # Validate product details
        for product in created_order.items:
            if product.item == "Product_5252":
                self.assertEqual(product.width, 113)
                self.assertEqual(product.height, 208)
                self.assertEqual(product.length, 113)
                self.assertEqual(product.weight, 900.0)
            elif product.item == "Product_2037":
                self.assertEqual(product.width, 45)
                self.assertEqual(product.height, 243)
                self.assertEqual(product.length, 113)
                self.assertEqual(product.weight, 560.0)


    def test_create_order_skips_missing_product(self):
        # Initialize OrderManager
        order_manager = OrderManager()

        # Mock product data returned by `load_products`
        mocked_products_data = [
            {"ID": "Product_5252", "Width": 113, "Height": 208, "Length": 113, "Weight": 900.0, "Fit ratio": 100},
        ]

        # Mock load_products method
        order_manager.load_products = MagicMock(return_value=mocked_products_data)

        # Mocked order with one valid and one missing product
        mocked_order_data = [
            {"Ordernr": "12345", "Date": "5-12-2024 14:00", "ID": "NonExistentProduct", "Picked": 1,
             "Location": "06C01"},
            {"Ordernr": "12345", "Date": "5-12-2024 14:00", "ID": "Product_5252", "Picked": 2, "Location": "07C01"},
        ]

        # Create the order
        order = order_manager.create_order(mocked_order_data)

        # Validate that only the valid product was added
        self.assertEqual(len(order.items), 2)
        self.assertTrue(all(product.item == "Product_5252" for product in order.items))

