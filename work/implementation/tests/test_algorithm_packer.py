import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from implementation.algorithm import BoxInputReader, BoxResult, Order, Packer, Product

# IMPORT FILE USING REFLECTION
current_dir = os.path.dirname(os.path.abspath(__file__))

class TestPacker(unittest.TestCase):

    def setUp(self):
        # Load product definitions from CSV
        self.products = []
        self.file_path = os.path.join(current_dir, 'test_files/dummy_box_definition.json')
        self.boxes = BoxInputReader.load_boxes(self.file_path)
        
        # Initialize Packer
        self.packer = Packer()
        product1 = Product(100, 100, 100, 50, 100, "Coca cola", "Fontys")
        products = [product1]
        self.order = Order("NMR230201", "1990-01-01", products)

    def test_pack_products(self):
        # Call the method
        coordinates = self.packer.pack_order(self.order, self.boxes)
        lines = coordinates.split("\n")

        # Assert the header line is present
        self.assertIn(
            ",XSD,115,236,115,Coca cola,100,100,100,0,0,0",
            lines[0],
        )

        # Assert only one product is packed
        self.assertEqual(len(lines), 1)  # One product line

    def test_get_packer_csv_result(self):
        # Call the method
        self.packer.pack_order(self.order, self.boxes)
        coordinates =  self.packer.get_packer_csv_result()
        self.assertEqual(len(coordinates.split("\n")), 1) # One product line

    def test_initial_box_selection_undersized(self):
        too_small = Product(10, 10, 10, 50, 100, "Too small", "Fontys")
        order = Order("NMR230201", "1990-01-01", [too_small])

        packer = Packer()
        packer.sorted_boxes = sorted(self.boxes, key=lambda box: box.max_volume(), reverse=False) 
        packer.order = order

        result = packer.initial_box_selection()

        self.assertIn("XXS", result.container_type)

    def test_initial_box_selection_oversized(self):
        too_big = Product(1000, 1000, 1000, 50, 100, "Too big", "Fontys")
        order = Order("NMR230201", "1990-01-01", [too_big])

        packer = Packer()
        packer.sorted_boxes = sorted(self.boxes, key=lambda box: box.max_volume(), reverse=False) 
        packer.order = order

        result = packer.initial_box_selection()

        self.assertIn("L", result.container_type)
        self.assertIn("L", packer.initial_box_selection(result).container_type)
        self.assertIn("L", packer.initial_box_selection(self.boxes[2]).container_type)

    def test_should_use_next_box(self):
        # Test when shouldUseNextBox is set to False
        too_big = Product(1000, 1000, 1000, 50, 100, "Too big", "Fontys")
        order = Order("NMR230201", "1990-01-01", [too_big])

        packer = Packer()
        packer.sorted_boxes = sorted(self.boxes, key=lambda box: box.max_volume(), reverse=False)
        packer.order = order

        with self.assertRaises(Exception) as context:
            packer.pack_order(order, self.boxes)

        self.assertTrue("Some products do not fit in any of the available boxes." in str(context.exception))

    def test_reset_all_items(self):
        # Test reset_all_items method
        product1 = Product(100, 100, 100, 50, 100, "Coca cola", "Fontys")
        product2 = Product(200, 200, 200, 50, 100, "Pepsi", "Fontys")
        order = Order("NMR230201", "1990-01-01", [product1, product2])

        packer = Packer()
        packer.sorted_boxes = sorted(self.boxes, key=lambda box: box.max_volume(), reverse=False)
        packer.order = order

        packer.pack_order(order, self.boxes)
        self.assertEqual(len(order.packed_items), 2)
