import os
import sys
import unittest
# IMPORT FILE USING REFLECTION
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from implementation.visualization import Reader

class TestCSVReader(unittest.TestCase):



    def test_load_orders_success(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(current_dir, 'test_files', 'orders_with_boxes_and_items.csv')
        
        # Load orders from the CSV file
        reader = Reader()
        orders = reader.load_orders_from_csv(csv_file_path)
        order1 = orders[0]
        # Assertions to verify the orders were loaded correctly
        self.assertEqual(len(orders), 6)
        self.assertEqual(order1.order_id, "1")
        self.assertEqual(len(order1.boxes), 2)
        self.assertEqual(len(order1.boxes[0].items), 2)
        self.assertEqual(orders[0].boxes[0].items[0].name, "Item A")
        self.assertEqual(orders[1].order_id, "2")
        self.assertEqual(orders[1].boxes[0].items[0].name, "Item D")


