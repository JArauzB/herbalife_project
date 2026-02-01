import sys
import os
import unittest
# IMPORT FILE USING REFLECTION
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from implementation.visualization import Box, Item

class TestBox(unittest.TestCase):

    def setUp(self):
        """Set up a new Box object for testing."""
        self.box = Box(box_id=1)
        self.item1 = Item("Laptop", weight=2.5, dimension=[15, 10, 1])
        self.item2 = Item("Book", weight=1.0, dimension=[8, 5, 1])

    def test_initialization(self):
        """Test that a Box object initializes with the correct attributes."""
        self.assertEqual(self.box.get_box_id(), 1)
        self.assertEqual(self.box.get_items(), [])

    def test_add_item(self):
        """Test that adding an item works correctly."""
        self.box.add_item(self.item1)
        self.assertIn(self.item1, self.box.get_items())
        self.assertEqual(len(self.box.get_items()), 1)

        self.box.add_item(self.item2)
        self.assertIn(self.item2, self.box.get_items())
        self.assertEqual(len(self.box.get_items()), 2)

    def test_get_box_name(self):
        self.assertEqual(self.box.get_box_name(), "")

    def test_get_count_items(self):
        self.box.add_item(self.item1)
        self.assertEqual(self.box.count_items(), 1)

    def test_repr(self):
        """Test the __repr__ method."""
        self.box.add_item(self.item1)
        self.assertEqual(repr(self.box), f"Box(id=1, items=[{repr(self.item1)}])")

    def test_str(self):
        """Test the __str__ method."""
        self.box.add_item(self.item1)
        self.box.add_item(self.item2)
        self.assertEqual(str(self.box), f"Box(id=1, items=[{self.item1}, {self.item2}])")

    def test_getters(self):
        """Test the getter methods."""
        self.box.add_item(self.item1)
        self.assertEqual(self.box.get_box_id(), 1)
        self.assertEqual(self.box.get_items(), [self.item1])


