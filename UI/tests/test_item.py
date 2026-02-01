import sys
import os
import unittest
sys.dont_write_bytecode = True

# IMPORT FILE USING REFLECTION
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import import_classes

modules = import_classes.import_all_modules_in_current_folder("item")
Item = getattr(modules['item'], 'Item', None)


# CREATE TESTS USING Arrange, Act, Assert

class TestItem(unittest.TestCase):
    
    def setUp(self):
        """Set up a sample item to use in multiple tests."""
        self.item = Item(name="Laptop", weight=2.5)

    def test_initialization(self):
        """Test if the Item is initialized correctly."""
        self.assertEqual(self.item.name, "Laptop")
        self.assertEqual(self.item.weight, 2.5)
        self.assertEqual(self.item.dimension, [0, 0, 0])  # Default dimension
        self.assertEqual(self.item.position, [0, 0, 0])   # Default position

    def test_dimension_setter_getter(self):
        """Test the setter and getter for dimension."""
        self.item.dimension = [30, 20, 3]
        self.assertEqual(self.item.dimension, [30, 20, 3])

        # Test invalid dimension (not a list of 3 numbers)
        with self.assertRaises(ValueError):
            self.item.dimension = [30, 20]  # Only two values

        with self.assertRaises(ValueError):
            self.item.dimension = [30, 'twenty', 3]  # Invalid value (string)

    def test_position_setter_getter(self):
        """Test the setter and getter for position."""
        self.item.position = [10, 5, 1]
        self.assertEqual(self.item.position, [10, 5, 1])

        # Test invalid position (not a list of 3 numbers)
        with self.assertRaises(ValueError):
            self.item.position = [10, 5]  # Only two values

        with self.assertRaises(ValueError):
            self.item.position = [10, 'five', 1]  # Invalid value (string)

    def test_repr(self):
        """Test the __repr__ method for correct formatting."""
        self.item.dimension = [30, 20, 3]
        self.item.position = [10, 5, 1]
        expected_repr = "Item(name=Laptop, weight=2.5, dimension=[30, 20, 3], position=[10, 5, 1])"
        self.assertEqual(repr(self.item), expected_repr)

if __name__ == "__main__":
    unittest.main()