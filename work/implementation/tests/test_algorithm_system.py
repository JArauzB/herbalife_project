from multiprocessing import Manager
import unittest
import os
import sys

from implementation.algorithm import BoxInputReader, Order, Product
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from implementation.algorithm import System

class TestSystem(unittest.TestCase):
    def setUp(self):
        self.orderline_file_path = './data/demo_order.csv'
        self.product_file_path = './data/demo_products.csv'
        self.output_file_path = './data/demo_output.csv'
      
    def test_static_method(self):
        # Arrange
        product = Product(1, 1, 1, 1, 100, "small", "NONE")
        orders = [Order("number", "0", [product])]
        boxes = BoxInputReader().load_boxes()

        # Act
        with Manager() as manager:
            progress_counter = manager.Value('i', 0)  # Shared counter initialized to 0
            lock = manager.Lock()  # Use Manager's Lock for multiprocessing

            result = System.pack_orders_in_chunk(orders, boxes, progress_counter, len(orders), lock)

        # Process the result
        packer, worker_time = result
        order_results = packer.get_packer_csv_result()

        # Assert
        self.assertIsInstance(worker_time, float)
        self.assertEqual(len(order_results.split('\n')), 1)  # 1 item
        self.assertIn(',XXS,1,1,1,small,1,1,1,0,0,0', order_results)

    def test_process_success(self):
        # Arrange
        system = System(self.output_file_path)
        output = None
        current_dir = os.path.dirname(os.path.abspath(__file__))
        combined_path = os.path.join(current_dir, '../algorithm', self.output_file_path)

        # Act
        system.start_processing(self.orderline_file_path, self.product_file_path)

        with open(combined_path, 'r') as file:
            output = file.readlines()

        # Assert
        self.assertTrue(len(system.packers) > 0)
        self.assertEqual(len(output), 8)
        self.assertEqual(output[0].strip(), 'Order ID,Box ID,Box Type,Box Width,Box Height,Box Depth,Item Name,Item Width,Item Height,Item Depth,Item Position X,Item Position Y,Item Position Z')
      