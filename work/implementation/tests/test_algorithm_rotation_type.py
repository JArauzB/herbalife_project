import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from implementation.algorithm import RotationType

class TestRotationType(unittest.TestCase):
    def setUp(self):
        self.rotation = RotationType.RT1

    def test_initial_rotation(self):
        self.assertEqual(self.rotation.value, RotationType.RT1.value)
    
    def test_min_value(self):
        self.assertEqual(self.rotation.min_value(), RotationType.RT1.value)

    def test_max_value(self):
        self.assertEqual(self.rotation.max_value(), RotationType.RT6.value)

    def test_next_rotation(self):
        self.assertEqual(self.rotation.value, RotationType.RT1.value)
        self.rotation = self.rotation.next_rotation()
        self.assertEqual(self.rotation.value, RotationType.RT2.value)
        self.rotation = self.rotation.next_rotation()
        self.assertEqual(self.rotation.value, RotationType.RT3.value)
        self.rotation = self.rotation.next_rotation()
        self.assertEqual(self.rotation.value, RotationType.RT4.value)
        self.rotation = self.rotation.next_rotation()
        self.assertEqual(self.rotation.value, RotationType.RT5.value)
        self.rotation = self.rotation.next_rotation()
        self.assertEqual(self.rotation.value, RotationType.RT6.value)
        self.rotation = self.rotation.next_rotation()
        self.assertEqual(self.rotation.value, RotationType.RT1.value)

    def test_previous_rotation(self):
        self.assertEqual(self.rotation.value, RotationType.RT1.value)
        self.rotation = self.rotation.previous_rotation()
        self.assertEqual(self.rotation.value, RotationType.RT6.value)
        self.rotation = self.rotation.previous_rotation()
        self.assertEqual(self.rotation.value, RotationType.RT5.value)
        self.rotation = self.rotation.previous_rotation()
        self.assertEqual(self.rotation.value, RotationType.RT4.value)
        self.rotation = self.rotation.previous_rotation()
        self.assertEqual(self.rotation.value, RotationType.RT3.value)
        self.rotation = self.rotation.previous_rotation()
        self.assertEqual(self.rotation.value, RotationType.RT2.value)
        self.rotation = self.rotation.previous_rotation()
        self.assertEqual(self.rotation.value, RotationType.RT1.value)
    
    def test_initial_rotation_dimensions_equal(self):
        self.assertEqual(self.rotation.initial_rotation(1, 1, 1).value, RotationType.RT1.value)

    def test_initial_rotation_dimensions_different(self):
        self.assertEqual(self.rotation.initial_rotation(2, 1, 3).value, RotationType.RT1.value)
        self.assertEqual(self.rotation.initial_rotation(3, 1, 2).value, RotationType.RT2.value)
        self.assertEqual(self.rotation.initial_rotation(1, 2, 3).value, RotationType.RT3.value)
        self.assertEqual(self.rotation.initial_rotation(1, 3, 2).value, RotationType.RT4.value)
        self.assertEqual(self.rotation.initial_rotation(3, 2, 1).value, RotationType.RT5.value)
        self.assertEqual(self.rotation.initial_rotation(2, 3, 1).value, RotationType.RT6.value)

    def test_initial_rotation_dimensions_near_equal(self):
        self.assertEqual(self.rotation.initial_rotation(2, 1, 2).value, RotationType.RT1.value)
        self.assertEqual(self.rotation.initial_rotation(1, 2, 2).value, RotationType.RT3.value)
        self.assertEqual(self.rotation.initial_rotation(2, 2, 1).value, RotationType.RT5.value)

    def test_adjust_dimensions_next(self):
        self.rotation.initial_rotation(3, 1, 2)
        self.assertEqual(self.rotation.adjust_dimensions(3, 1, 2), (3, 1, 2))
        self.rotation = self.rotation.next_rotation()
        self.assertEqual(self.rotation.adjust_dimensions(3, 1, 2), (2, 1, 3))
        self.rotation = self.rotation.next_rotation()
        self.assertEqual(self.rotation.adjust_dimensions(3, 1, 2), (1, 3, 2))
        self.rotation = self.rotation.next_rotation()
        self.assertEqual(self.rotation.adjust_dimensions(3, 1, 2), (2, 3, 1))
        self.rotation = self.rotation.next_rotation()
        self.assertEqual(self.rotation.adjust_dimensions(3, 1, 2), (1, 2, 3))
        self.rotation = self.rotation.next_rotation()
        self.assertEqual(self.rotation.adjust_dimensions(3, 1, 2), (3, 2, 1))
        self.rotation = self.rotation.next_rotation()
        self.assertEqual(self.rotation.adjust_dimensions(3, 1, 2), (3, 1, 2))

    def test_adjust_dimensions_previous(self):
        self.rotation.initial_rotation(3, 1, 2)
        self.assertEqual(self.rotation.adjust_dimensions(3, 1, 2), (3, 1, 2))
        self.rotation = self.rotation.previous_rotation()
        self.assertEqual(self.rotation.adjust_dimensions(3, 1, 2), (3, 2, 1))
        self.rotation = self.rotation.previous_rotation()
        self.assertEqual(self.rotation.adjust_dimensions(3, 1, 2), (1, 2, 3))
        self.rotation = self.rotation.previous_rotation()
        self.assertEqual(self.rotation.adjust_dimensions(3, 1, 2), (2, 3, 1))
        self.rotation = self.rotation.previous_rotation()
        self.assertEqual(self.rotation.adjust_dimensions(3, 1, 2), (1, 3, 2))
        self.rotation = self.rotation.previous_rotation()
        self.assertEqual(self.rotation.adjust_dimensions(3, 1, 2), (2, 1, 3))
        self.rotation = self.rotation.previous_rotation()
        self.assertEqual(self.rotation.adjust_dimensions(3, 1, 2), (3, 1, 2))

    def test_adjust_dimensions_initial_rotations(self):
        self.assertEqual(self.rotation.initial_rotation(3, 1, 2).adjust_dimensions(3, 1, 2), (2, 1, 3))
        self.assertEqual(self.rotation.initial_rotation(3, 2, 1).adjust_dimensions(3, 2, 1), (2, 1, 3))
        self.assertEqual(self.rotation.initial_rotation(2, 3, 1).adjust_dimensions(2, 3, 1), (2, 1, 3))
        self.assertEqual(self.rotation.initial_rotation(2, 1, 3).adjust_dimensions(2, 1, 3), (2, 1, 3))
        self.assertEqual(self.rotation.initial_rotation(1, 2, 3).adjust_dimensions(1, 2, 3), (2, 1, 3))
        self.assertEqual(self.rotation.initial_rotation(1, 3, 2).adjust_dimensions(1, 3, 2), (2, 1, 3))

    def test_initial_rotation_edge_cases(self):
        self.assertEqual(self.rotation.initial_rotation(0, 0, 0).value, RotationType.RT1.value)
        self.assertEqual(self.rotation.initial_rotation(0, 0, 1).value, RotationType.RT1.value)
        self.assertEqual(self.rotation.initial_rotation(1, 0, 1).value, RotationType.RT1.value)
        self.assertEqual(self.rotation.initial_rotation(1, 0, 0).value, RotationType.RT2.value)
        self.assertEqual(self.rotation.initial_rotation(0, 1, 1).value, RotationType.RT3.value)
        self.assertEqual(self.rotation.initial_rotation(0, 1, 0).value, RotationType.RT4.value)
        self.assertEqual(self.rotation.initial_rotation(1, 1, 0).value, RotationType.RT5.value)

    def test_adjust_dimensions_edge_cases(self):
        self.rotation.initial_rotation(0, 0, 0)
        self.assertEqual(self.rotation.adjust_dimensions(0, 0, 0), (0, 0, 0))
        self.rotation = self.rotation.next_rotation()
        self.assertEqual(self.rotation.adjust_dimensions(0, 0, 0), (0, 0, 0))
        self.rotation = self.rotation.next_rotation()
        self.assertEqual(self.rotation.adjust_dimensions(0, 0, 0), (0, 0, 0))
        self.rotation = self.rotation.next_rotation()
        self.assertEqual(self.rotation.adjust_dimensions(0, 0, 0), (0, 0, 0))
        self.rotation = self.rotation.next_rotation()
        self.assertEqual(self.rotation.adjust_dimensions(0, 0, 0), (0, 0, 0))
        self.rotation = self.rotation.next_rotation()
        self.assertEqual(self.rotation.adjust_dimensions(0, 0, 0), (0, 0, 0))
        self.rotation = self.rotation.next_rotation()
        self.assertEqual(self.rotation.adjust_dimensions(0, 0, 0), (0, 0, 0))
