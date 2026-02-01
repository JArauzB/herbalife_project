import unittest
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from implementation.algorithm import BoxDefinition, Product
import unittest
import sys
import logging
from implementation.algorithm import BoxDefinition, Product, BoxResult, Order, Position, RotationType, LayerResult

current_dir = os.path.dirname(os.path.abspath(__file__))

class TestBoxResult(unittest.TestCase):
    """
    Test the BoxResult class.
    """

    def setUp(self):
        self.box_definition = BoxDefinition(
            length=410,
            height=300,
            width=240,
            weight=430,
            max_weight=19570,
            description="Carton small",
            container_type="S",
            remark="Small cartons 6006380V1-00",
            max_fill_percentage=80.0,
            min_fill_percentage=5.0
        )
        self.product1 = Product(10, 20, 30, 500, 100, "Product1", 1)
        self.product2 = Product(15, 25, 35, 600, 100, "Product2", 1)
        self.box_result = BoxResult(self.box_definition)

    def test_add_product_to_box(self):
        position = Position(self.product1, 0, 0, 0, RotationType.initial_rotation(self.product1.width, self.product1.height, self.product1.length))
        self.assertTrue(self.box_result.add_product_to_box(self.product1))
        self.assertEqual(position, self.box_result.get_all_coordinates()[0])

    def test_add_new_layer(self):
        position = Position(self.product1, 0, 0, 0, RotationType.initial_rotation(self.product1.width, self.product1.height, self.product1.length))
        self.assertTrue(self.box_result.add_new_layer(position, []))
        self.assertEqual(len(self.box_result.get_layers()), 1)

    def test_add_new_layer_invalid_coordinates(self):
        with self.assertRaises(ValueError):
            position = Position(self.product1, 0, 0, 0, RotationType.initial_rotation(self.product1.width, self.product1.height, self.product1.length))
            position.coordinates = None  # Force invalid coordinates
            self.box_result.add_new_layer(position, [])

    def test_get_oversized_products(self):
        self.box_result.oversized_products.append(self.product1)
        self.assertIn(self.product1, self.box_result.get_oversized_products())

    def test_get_leftover_products(self):
        self.box_result.leftover_products.append(self.product2)
        self.assertIn(self.product2, self.box_result.get_leftover_products())

    def test_get_box_id(self):
        self.assertEqual(self.box_result.get_box_id(), id(self.box_result))

    def test_get_box_definition(self):
        self.assertEqual(self.box_result.get_box_definition(), self.box_definition)

    def test_get_layers(self):
        self.assertEqual(self.box_result.get_layers(), self.box_result.layers)

    def test_get_products_positions(self):
        # Add a product to the box
        position = Position(self.product1, 0, 0, 0, RotationType.initial_rotation(self.product1.width, self.product1.height, self.product1.length))
        self.box_result.add_new_layer(position, [])
        
        # Retrieve product positions
        products_positions = self.box_result.get_products_positions()
        
        # Check if the product positions are correctly retrieved
        self.assertEqual(len(products_positions), 1)
        self.assertEqual(products_positions[0]['product'], self.product1.item)
        self.assertEqual(products_positions[0]['starting_point'], (0, 0, 0))
        self.assertEqual(products_positions[0]['extending_point'], (self.product1.height, self.product1.width, self.product1.length))
        self.assertEqual(products_positions[0]['rotated_dimensions'], (self.product1.height, self.product1.width, self.product1.length))
        self.assertEqual(products_positions[0]['rotation'], RotationType.initial_rotation(self.product1.width, self.product1.height, self.product1.length).name)

    def test_get_products_positions_exception(self):
        # Force an exception by setting layers to None
        self.box_result.layers = None
        
        with self.assertRaises(Exception):
            self.box_result.get_products_positions()
            
    
    def test_pack_products_by_order(self):
        order = Order("OrderNumber", "0", [self.product1, self.product2])
        self.box_result.pack_products_by_order(order)
        
        # Check if products are packed
        self.assertIn(self.product1.item, [pos['product'] for pos in self.box_result.get_products_positions()])
        self.assertIn(self.product2.item, [pos['product'] for pos in self.box_result.get_products_positions()])

    def test_pack_products_by_order_with_rejected_items(self):
        oversized_product = Product(1000, 1000, 1000, 1000, 100, "OversizedProduct", 1)
        order = Order("OrderNumber", "0", [self.product1, oversized_product])
        self.box_result.pack_products_by_order(order)
        
        # Check if the oversized product is rejected
        self.assertIn(oversized_product, self.box_result.get_oversized_products())
        self.assertIn(self.product1.item, [pos['product'] for pos in self.box_result.get_products_positions()])

    def test_pack_products_by_order_empty_order(self):
        order = Order("OrderNumber", "0", [])
        self.box_result.pack_products_by_order(order)
        
        # Check if no products are packed
        self.assertEqual(len(self.box_result.get_products_positions()), 0)
