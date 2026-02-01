import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from implementation.algorithm import ProductInputReader

# IMPORT FILE USING REFLECTION
current_dir = os.path.dirname(os.path.abspath(__file__))

class TestProductInputReader(unittest.TestCase):
    def setUp(self):
        self.file_path = os.path.join(current_dir, './test_files/product_definitions.csv')
        self.reader = ProductInputReader()

    def test_read_csv(self):
        self.reader.read_csv(self.file_path)
        
        self.assertEqual(len(self.reader.get_data()), 5)

    def test_read_csv_no_reload(self):
        self.reader.read_csv(self.file_path)
        result = self.reader.read_csv(self.file_path)
        self.assertFalse(result)

    def test_get_data(self):
        self.reader.read_csv(self.file_path)
        data = self.reader.get_data()
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0]['ID'], '3359')
        self.assertEqual(data[3]['ID'], '3589')

    def test_singleton(self):
        reader1 = ProductInputReader()
        reader2 = ProductInputReader()
        self.assertIs(reader1, reader2)


