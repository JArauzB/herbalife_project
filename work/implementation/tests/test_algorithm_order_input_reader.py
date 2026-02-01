import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from implementation.algorithm import OrderInputReader

current_dir = os.path.dirname(os.path.abspath(__file__))

class TestOrderInputReader(unittest.TestCase):
    def setUp(self):
        self.file_path = os.path.join(current_dir, './test_files/order_with_few_items.csv')
        self.reader = OrderInputReader()

    def test_read_csv(self):
        self.reader.read_csv(self.file_path)
        
        self.assertEqual(len(self.reader.get_data()), 32)

    def test_read_csv_no_reload(self):
        self.reader.read_csv(self.file_path)
        result = self.reader.read_csv(self.file_path)
        self.assertFalse(result)

    def test_get_data(self):
        self.reader.read_csv(self.file_path)
        data = self.reader.get_data()
        self.assertEqual(len(data), 32)
        self.assertEqual(data[0]['Ordernr'], '5R02891084')
        self.assertEqual(data[10]['Ordernr'], '4G01018426')

    def test_singleton(self):
        reader1 = OrderInputReader()
        reader2 = OrderInputReader()
        self.assertIs(reader1, reader2)
