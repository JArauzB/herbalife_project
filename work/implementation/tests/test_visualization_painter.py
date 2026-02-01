import sys
import os
import unittest
from unittest.mock import MagicMock, patch
import matplotlib.pyplot as plt


# IMPORT FILE USING REFLECTION
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from implementation.visualization import Box, Item, Order, Painter



class TestPainter(unittest.TestCase):

    def setUp(self):
        """Set up a new Box object for testing."""
        self.order = Order(order_id=1)
        self.box = Box(box_id=1, dimension=[100, 200, 500])
        self.item1 = Item("Huawei 20", weight=2.5, dimension=[50, 50, 50], position=[0, 0, 0])
        self.item2 = Item("Apple 200", weight=1.0, dimension=[50, 50, 50], position=[0, 50, 0])
        
        # Add items to the box
        self.box.add_item(self.item1)
        self.box.add_item(self.item2)
        
        # Initialize Painter with the box
        self.painter = Painter(self.box)


    def test_initialization(self):
        """Test that Painter initializes with the correct box dimensions and items."""
        self.assertEqual(self.painter.width, 100)
        self.assertEqual(self.painter.height, 500)
        self.assertEqual(self.painter.length, 200)
        self.assertEqual(len(self.painter.items), 2)  # Ensure both items were added to the box

    def test_plotBoxAndItems(self):
        """Test that plotBoxAndItems returns a matplotlib Figure."""
        fig = self.painter.plotBoxAndItems(title="Test text", alpha=0.2, fontsize=5)

        # Check if fig is a matplotlib Figure instance
        self.assertIsInstance(fig, plt.Figure, "Expected a matplotlib Figure as output from plotBoxAndItems.")
        
        # fig.show()

    def test_items_added_to_box(self):
        """Test that items are correctly added to the box."""
        self.assertIn(self.item1, self.painter.items)
        self.assertIn(self.item2, self.painter.items)
        self.assertEqual(self.painter.items[0].position, [0, 0, 0])
        self.assertEqual(self.painter.items[1].position, [0, 50, 0])

