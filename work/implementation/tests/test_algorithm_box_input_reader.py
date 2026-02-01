import unittest
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from implementation.algorithm import BoxInputReader

current_dir = os.path.dirname(os.path.abspath(__file__))

class TestBoxInputReader(unittest.TestCase):
    """
    Test the BoxInputReader class.

    Methods:
        setUp: Initializes the test case.
        test_load_boxes_length: Tests the load_boxes method for length.
        test_load_boxes_height: Tests the load_boxes method for height.
        test_load_boxes_width: Tests the load_boxes method for width.
        test_load_boxes_weight: Tests the load_boxes method for weight.
        test_load_boxes_max_weight: Tests the load_boxes method for max_weight.
        test_load_boxes_description: Tests the load_boxes method for description.
        test_load_boxes_container_type: Tests the load_boxes method for container_type.
        test_load_boxes_remark: Tests the load_boxes method for remark.
        test_load_boxes_max_fill_percentage: Tests the load_boxes method for max_fill_percentage.
        test_load_boxes_min_fill_percentage: Tests the load_boxes method for min_fill_percentage.
    """
    
    def setUp(self):
        """
        Initializes the test case.
        """
        self.file_path = os.path.join(current_dir, './test_files/dummy_box_definition.json')
        self.boxes = BoxInputReader.load_boxes(self.file_path)

    def test_load_boxes_length(self):
        """
        Tests the load_boxes method for length.
        """
        self.assertEqual(self.boxes[0].length, 35)
        self.assertEqual(self.boxes[1].length, 400)

    def test_load_boxes_height(self):
        """
        Tests the load_boxes method for height.
        """
        self.assertEqual(self.boxes[0].height, 330)
        self.assertEqual(self.boxes[1].height, 510)

    def test_load_boxes_width(self):
        """
        Tests the load_boxes method for width.
        """
        self.assertEqual(self.boxes[0].width, 245)
        self.assertEqual(self.boxes[1].width, 415)

    def test_load_boxes_weight(self):
        """
        Tests the load_boxes method for weight.
        """
        self.assertEqual(self.boxes[0].weight, 30)
        self.assertEqual(self.boxes[1].weight, 905)

    def test_load_boxes_max_weight(self):
        """
        Tests the load_boxes method for max_weight.
        """
        self.assertEqual(self.boxes[0].max_weight, 19970)
        self.assertEqual(self.boxes[1].max_weight, 19095)

    def test_load_boxes_description(self):
        """
        Tests the load_boxes method for description.
        """
        self.assertEqual(self.boxes[0].description, "Envelope")
        self.assertEqual(self.boxes[1].description, "Carton large")

    def test_load_boxes_container_type(self):
        """
        Tests the load_boxes method for container_type.
        """
        self.assertEqual(self.boxes[0].container_type, "ENV")
        self.assertEqual(self.boxes[1].container_type, "L")

    def test_load_boxes_remark(self):
        """
        Tests the load_boxes method for remark.
        """
        self.assertEqual(self.boxes[0].remark, "Envelope")
        self.assertEqual(self.boxes[1].remark, "Large cartons 6006360A-00")

    def test_load_boxes_max_fill_percentage(self):
        """
        Tests the load_boxes method for max_fill_percentage.
        """
        self.assertEqual(self.boxes[0].max_fill_percentage, 80.0)
        self.assertEqual(self.boxes[1].max_fill_percentage, 80.0)

    def test_load_boxes_min_fill_percentage(self):
        """
        Tests the load_boxes method for min_fill_percentage.
        """
        self.assertEqual(self.boxes[0].min_fill_percentage, 5.0)
        self.assertEqual(self.boxes[1].min_fill_percentage, 5.0)
