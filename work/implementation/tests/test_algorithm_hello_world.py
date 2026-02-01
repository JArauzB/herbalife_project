import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from implementation.algorithm import HelloWorld

class TestHelloWorld(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(HelloWorld.hello(), "hello")  # Testing the actual hello() function
