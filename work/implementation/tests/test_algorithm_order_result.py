import unittest
import csv
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from implementation.algorithm import Order, Product, OrderResult, BoxResult, BoxDefinition

current_dir = os.path.dirname(os.path.abspath(__file__))

class TestOrderResult(unittest.TestCase):
    """
    Test the OrderResult class.
    
    The OrderResult class represents the results of the packing process.
    
    Methods:
        setUp: Initializes the test case.
        test_add_box: Test that the add_box method adds a box to the order result.
        test_get_boxes: Test that the get_boxes method returns the list of boxes in the order result.
        test_get_order: Test that the get_order method returns the order in the order result.
        test_get_csv_result: Test that the get_csv_result method returns the packing results in CSV format.
    """

    def setUp(self):
        """
        Initializes the OrderResult object with the specified order.
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
        self.order_result = OrderResult(self.order)

        self.box = BoxDefinition(length=30.0,height=20.0,width=10.0,weight=500.0,max_weight=10000.0,description="Test Box",container_type="Cardboard",remark="Handle with care",max_fill_percentage=90.0,min_fill_percentage=10.0)

    def test_add_box(self):
        """
        Test that the add_box method adds a box to the order result.
        """
        box = BoxResult(self.box)
        self.order_result.add_box(box)
        self.assertIn(box, self.order_result.get_boxes())

    def test_get_boxes(self):
        """
        Test that the get_boxes method returns the list of boxes in the order result.
        """
        box = BoxResult(self.box)
        self.order_result.add_box(box)
        boxes = self.order_result.get_boxes()
        self.assertEqual(boxes, [box])

    def test_get_order(self):
        """
        Test that the get_order method returns the order in the order result.
        """
        order = self.order_result.get_order()
        self.assertEqual(order, self.order)

    def test_get_csv_result(self):
        """
        Test that the get_csv_result method returns the packing results in CSV format.
        """
        box = BoxResult(self.box)
        self.order_result.add_box(box)
        csv_result = self.order_result.get_csv_result()
        self.assertIsInstance(csv_result, str)
