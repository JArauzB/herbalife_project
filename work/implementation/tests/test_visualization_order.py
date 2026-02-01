import sys
import os
import unittest

# IMPORT FILE USING REFLECTION
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from implementation.visualization import Box, Order


class TestOrder(unittest.TestCase):

    def setUp(self):
        """Set up a new Order object for testing."""
        self.order = Order(order_id=101)
        self.box1 = Box(box_id=1)
        self.box2 = Box(box_id=2)

    def test_initialization(self):
        """Test that an Order object initializes with the correct attributes."""
        self.assertEqual(self.order.get_order_id(), 101)
        self.assertEqual(self.order.get_boxes(), [])

    def test_add_box(self):
        """Test that adding a box works correctly."""
        self.order.add_box(self.box1)
        self.assertIn(self.box1, self.order.get_boxes())
        self.assertEqual(len(self.order.get_boxes()), 1)

        self.order.add_box(self.box2)
        self.assertIn(self.box2, self.order.get_boxes())
        self.assertEqual(len(self.order.get_boxes()), 2)

    def test_get_order_id(self):
        """Test the get_order_id method."""
        self.assertEqual(self.order.get_order_id(), 101)

    def test_get_boxes(self):
        """Test the get_boxes method."""
        self.order.add_box(self.box1)
        self.order.add_box(self.box2)
        self.assertEqual(self.order.get_boxes(), [self.box1, self.box2])

    def test_count_boxes(self):
        """Test to get count of boxes."""
        self.order.add_box(self.box1)
        self.order.add_box(self.box2)
        self.assertEqual(self.order.count_boxes(), 2)

    def test_repr(self):
        """Test the __repr__ method."""
        self.order.add_box(self.box1)
        expected_repr = f"Order(id={self.order.order_id}, boxes=[{self.box1}])"
        self.assertEqual(repr(self.order), expected_repr)



