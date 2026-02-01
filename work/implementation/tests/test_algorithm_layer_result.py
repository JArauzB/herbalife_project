import logging
import unittest
import json
import pandas as pd
import os

from implementation.algorithm.box_definition import BoxDefinition
from implementation.algorithm.product import Product
from implementation.algorithm.layer_result import LayerResult, check_collision
from implementation.algorithm.box_result import BoxResult
from implementation.algorithm.position import Position
from implementation.algorithm.rotation_type import RotationType
from implementation.algorithm.fragment import Fragment
from implementation.algorithm.order import Order
from implementation.algorithm.packer import Packer

class TestLayerAndBoxResult(unittest.TestCase):
    @classmethod
    def setUpClass(cls):

        """
        Set up resources needed for all test cases in this class.

        - Loads JSON box definitions to simulate available box types.
        - Loads CSV data containing product information and orders.
        """

        # Paths to the JSON and CSV test files
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, 'test_files', 'dummy_box_definition.json')
        csv_path = os.path.join(current_dir, 'test_files', 'orders_with_dimensions.csv')

        # Load JSON box definitions
        with open(json_path, 'r') as f:
            cls.box_definitions = json.load(f)

        # Create a dictionary for quick lookup by container_type
        cls.box_lookup = {box['container_type']: BoxDefinition(
            length=box['length'],
            height=box['height'],
            width=box['width'],
            weight=box['weight'],
            max_weight=box['max_weight'],
            description=box['description'],
            container_type=box['container_type'],
            remark=box['remark'],
            max_fill_percentage=box['max_fill_percentage'],
            min_fill_percentage=box['min_fill_percentage']
        ) for box in cls.box_definitions}

        # Load CSV data and prepare Product objects
        cls.data = pd.read_csv(csv_path)
        cls.grouped_orders = cls.data.groupby('Ordernr')

    def test_box_result_with_csv_data(self):

        """
        Test if products from CSV orders can be added to a box correctly.

        For each order in the CSV:
        - Determines the box type from the order's "Box Name".
        - Initializes a `BoxResult` with the corresponding box definition.
        - Processes all products in the order to check if they fit in the box.
        - Adds products to the box or skips them if they don't fit.
        - Asserts that at least one layer is created and the box has a non-zero volume.
        """

        # Group data by orders to test each order separately
        for ordernr, group in self.data.groupby('Ordernr'):
            print(f"Testing Order: {ordernr}")

            # Get the box type for the order
            box_name = group['Box Name'].iloc[0]

            # Initialize BoxResult with the corresponding box
            test_box = self.box_lookup[box_name]
            box_result = BoxResult(test_box)

            # Process each product in the order
            for _, row in group.iterrows():
                product = Product(
                    width=row['Width'],
                    height=row['Height'],
                    length=row['Length'],
                    weight=row['Weight_x'],  # Weight from the CSV
                    fit_ratio=row['Fit ratio'],  # Fit ratio from the CSV
                    item=row['ID'],
                    location=row['Location']
                )

                # Add product to the box and check if it fits
                product_added = box_result.add_product_to_box(product)
                if product_added:
                    print(f"Product {product.get_product_name()} added to the box.")
                else:
                    print(f"Product {product.get_product_name()} does not fit in the box.")



            # Ensure at least one layer is created and has products
            self.assertGreater(len(box_result.get_layers()), 0, f"Order {ordernr} should create at least one layer.")

    def test_product_exceeds_box_constraints(self):
        # Test that a product exceeding box constraints does not fit
        box = self.box_lookup["M"]
        box_result = BoxResult(box)

        # Create a product that exceeds the box constraints
        oversized_product = Product(
            width=box.width + 10,  # Width exceeds box width
            height=box.height + 10,  # Height exceeds box height
            length=box.length + 10,  # Length exceeds box length
            weight=box.max_weight + 10,  # Weight exceeds max weight
            fit_ratio=100,
            item="OversizedProduct",
            location="TestLocation"
        )
        product_added = box_result.add_product_to_box(oversized_product)
        self.assertFalse(product_added, "Oversized product should not fit in the box.")

    def test_hardcoded_box_packing_small_7items1(self):
        """
        Test packing hardcoded products into a specified box size.
        """
    
        # Define the box
        box = BoxDefinition(
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
    
        # Define the hardcoded products
        products = [
            Product(width=53, height=97, length=53, weight=74.0, fit_ratio=100, item="Product_5819", location="21C27"),
            Product(width=50, height=180, length=50, weight=230.0, fit_ratio=100, item="Product_3573",
                    location="32C25"),
            Product(width=138, height=210, length=138, weight=1139.0, fit_ratio=100, item="Product_3410",
                    location="06B04"),
            Product(width=100, height=190, length=100, weight=640.0, fit_ratio=100, item="Product_5235",
                    location="02C12"),
            Product(width=50, height=180, length=50, weight=228.0, fit_ratio=100, item="Product_3574",
                    location="15C28"),
            Product(width=50, height=210, length=50, weight=284.0, fit_ratio=100, item="Product_3575",
                    location="13B10"),
            Product(width=145, height=27, length=83, weight=69.0, fit_ratio=100, item="Product_4938", location="15C14")
        ]
    
        # Sort products by volume
        products = sorted(products, key=lambda p: p.volume(), reverse=True)
    
        # Create a box result object
        box_result = BoxResult(box)
    
        # Attempt to pack products
        for product in products:
            box_result.add_product_to_box(product)
        
        # Verify oversized products
        expected_oversized = []  # None of the products are oversized relative to the box
        oversized_ids = [product.get_product_name() for product in box_result.get_oversized_products()]
        self.assertEqual(oversized_ids, expected_oversized, "Unexpected oversized products")
    
        # Verify leftover products
        expected_leftovers = []  # This product couldn't fit after placing others
        leftover_ids = [product.get_product_name() for product in box_result.get_leftover_products()]
        self.assertEqual(leftover_ids, expected_leftovers, "Expected no leftover products")
    
        # Assert remaining products are packed successfully
        packed_products = [position.get_product() for layer in box_result.get_layers() for position in layer.get_positions()]
        for product in products:
            if product.get_product_name() not in oversized_ids and product.get_product_name() not in leftover_ids:
                with self.subTest(product=product.get_product_name()):
                    self.assertIn(product, packed_products, f"Product {product.get_product_name()} should be packed in the box.")
    
        # Log the layers and products for clarity
        logging.info(f"Packed Layers: {len(box_result.get_layers())}")
        for idx, layer in enumerate(box_result.get_layers()):
            logging.info(f"Layer {idx + 1}: {[p.get_product().get_product_name() for p in layer.get_positions()]}")

    def test_hardcoded_box_packing_medium_7items(self):
        """
        Test packing hardcoded products into a specified box size.
        """
    
        # Define the box
        box = BoxDefinition(
            length=510,
            height=300,
            width=415,
            weight=805,
            max_weight=19195,
            description="Carton medium",
            container_type="M",
            remark="Medium 6006380V1-00",
            max_fill_percentage=80.0,
            min_fill_percentage=5.0
        )
    
        # Define the hardcoded products based on provided data
        products = [
            Product(width=113, height=208, length=113, weight=900.0, fit_ratio=100, item="Product_5252",
                    location="06C01"),
            Product(width=45, height=243, length=113, weight=560.0, fit_ratio=100, item="Product_2037",
                    location="06D09"),
            Product(width=100, height=190, length=100, weight=665.0, fit_ratio=100, item="Product_5591",
                    location="09C06"),
            Product(width=138, height=210, length=138, weight=1139.0, fit_ratio=100, item="Product_3410",
                    location="06B04"),
            Product(width=100, height=120, length=100, weight=305.0, fit_ratio=100, item="Product_2026",
                    location="07C13"),
            Product(width=100, height=102, length=100, weight=282.0, fit_ratio=100, item="Product_4918",
                    location="07D11"),
            Product(width=260, height=145, length=345, weight=2518.0, fit_ratio=100, item="Product_5028",
                    location="07D06")
        ]

# #region debug
        # order = Order("TestOrder", "0", products)
        # packer = Packer()
        # result = packer.pack_order(order, [box])
        # print(f"\n\n\n\n\n\n\n\n\n\n\n{result}\n\n\n\n\n\n\n\n\n\n")
# #endregion end debug
    
        # Initialize BoxResult and pack products
        order = Order("TestOrder", "0", products)
        box_result = BoxResult(box)
        box_result.pack_products_by_order(order)
    
        # Assertions for oversized and leftover products
        oversized_ids = [product.get_product_name() for product in box_result.get_oversized_products()]
        leftover_ids = [product.get_product_name() for product in box_result.get_leftover_products()]
    
        self.assertEqual(oversized_ids, [], "Unexpected oversized products")
        self.assertEqual(leftover_ids, [], "Unexpected leftover products")

    def test_hardcoded_box_packing_medium_7items2(self):
        """
        Test packing hardcoded products into a medium box size.
        """
    
        # Define the box
        box = BoxDefinition(
            length=510,
            height=300,
            width=415,
            weight=805,
            max_weight=19195,
            description="Carton medium",
            container_type="M",
            remark="Medium 6006380V1-00",
            max_fill_percentage=80.0,
            min_fill_percentage=5.0
        )
    
        # Define the hardcoded products based on provided data
        products = [
            Product(width=113, height=208, length=113, weight=900.0, fit_ratio=100, item="Product_5252",
                    location="06C01"),
            Product(width=45, height=243, length=113, weight=560.0, fit_ratio=100, item="Product_2037",
                    location="06D09"),
            Product(width=100, height=190, length=100, weight=665.0, fit_ratio=100, item="Product_5591",
                    location="09C06"),
            Product(width=138, height=210, length=138, weight=1139.0, fit_ratio=100, item="Product_3410",
                    location="06B04"),
            Product(width=100, height=120, length=100, weight=305.0, fit_ratio=100, item="Product_2026",
                    location="07C13"),
            Product(width=100, height=102, length=100, weight=282.0, fit_ratio=100, item="Product_4918",
                    location="07D11"),
            Product(width=260, height=145, length=345, weight=2518.0, fit_ratio=100, item="Product_5028",
                    location="07D06")
        ]
    
        # Initialize BoxResult and pack products
        order = Order("TestOrder", "0", products)
        box_result = BoxResult(box)
        box_result.pack_products_by_order(order)
    
        # Assertions for oversized and leftover products
        oversized_ids = [product.get_product_name() for product in box_result.get_oversized_products()]
        leftover_ids = [product.get_product_name() for product in box_result.get_leftover_products()]
    
        # Assert that no products are oversized
        self.assertEqual(oversized_ids, [], "Unexpected oversized products")
    
        self.assertEqual(leftover_ids, [], "All products should fit into the medium box.")
    
        # Additional logging for clarity (optional)
        positions = [position for layer in box_result.get_layers() for position in layer.get_positions()]
        logging.info(f"Packed Products: {[p.get_product().get_product_name() for p in positions]}")
        logging.info(f"Leftover Products: {leftover_ids}")
        logging.info(f"Oversized Products: {oversized_ids}")
    
        # Log the layers and packed products
        logging.info(f"Packed Layers: {len(box_result.get_layers())}")
        for idx, layer in enumerate(box_result.get_layers()):
            logging.info(f"Layer {idx + 1}: {[p.get_product().get_product_name() for p in layer.get_positions()]}")
    
    def test_hardcoded_box_packing_medium_7items_fit(self):
        box = BoxDefinition(
            length=510,
            height=300,
            width=415,
            weight=805,
            max_weight=19195,
            description="Carton medium",
            container_type="M",
            remark="Medium 6006380V1-00",
            max_fill_percentage=80.0,
            min_fill_percentage=5.0
        )
    
        products = [
            Product(width=113, height=208, length=113, weight=900.0, fit_ratio=100, item="Product_5252",location="06C01"),
            Product(width=45, height=243, length=113, weight=560.0, fit_ratio=100, item="Product_2037",location="06C01"),
            Product(width=100, height=190, length=100, weight=665.0, fit_ratio=100, item="Product_5591",location="06C01"),
            Product(width=138, height=210, length=138, weight=1139.0, fit_ratio=100, item="Product_3410",location="06C01"),
            Product(width=100, height=120, length=100, weight=305.0, fit_ratio=100, item="Product_2026",location="06C01"),
            Product(width=100, height=102, length=100, weight=282.0, fit_ratio=100, item="Product_4918",location="06C01"),
            Product(width=260, height=145, length=345, weight=2518.0, fit_ratio=100, item="Product_5028",location="06C01"),
        ]
    
        order = Order("TestOrder", "0", products)
        box_result = BoxResult(box)
        box_result.pack_products_by_order(order)
    
        # Check no leftover or oversized products
        self.assertEqual(box_result.get_oversized_products(), [], "No oversized products should exist.")
        self.assertEqual(box_result.get_leftover_products(), [], "All products should fit into the box.")
    
        # Log the layers and products for clarity
        logging.info(f"Layers: {len(box_result.get_layers())}")
        for idx, layer in enumerate(box_result.get_layers()):
            logging.info(f"Layer {idx + 1}: {[position.get_product().get_product_name() for position in layer.get_positions()]}")

    def test_check_collision(self):
        # Create a box
        box = BoxDefinition(width=500, height=500, length=500,weight=805,
            max_weight=19195,
            description="Carton medium",
            container_type="M",
            remark="Medium 6006380V1-00",
            max_fill_percentage=80.0,
            min_fill_percentage=5.0)
    
        # Create the layer
        layer = LayerResult(box)
    
        # Add a product to the layer
        product1 = Product(width=100, height=100, length=100, weight=10, fit_ratio=100, item="Product1",location="06C01")

        position1 = Position(product1, 0, 0, 0, RotationType.initial_rotation(*(product1.get_dimensions())))

        layer.get_positions().append(position1)
    
        # Collect existing coordinates
        existing_coordinates = layer.get_product_coordinates()
    
        # Create another product
        product2 = Product(width=100, height=100, length=100, weight=10, fit_ratio=100, item="Product2",location="06C01")

        position2 = Position(product2, 50, 50, 50, RotationType.initial_rotation(*(product2.get_dimensions())))
    
        # Test collision
        self.assertTrue(
            check_collision(position2, existing_coordinates),
            "Expected a collision between Product1 and Product2."
        )
    
        # Place a non-overlapping product
        product3 = Product(width=100, height=100, length=100, weight=10, fit_ratio=100, item="Product3",location="06C01")

        position3 = Position(product3, 200, 200, 200, RotationType.initial_rotation(*(product3.get_dimensions())))
    
        # Test no collision
        self.assertFalse(
            check_collision(position3, existing_coordinates),
            "Expected no collision between Product1 and Product3."
        )

    def test_split_space_around_product(self):
        # Define the box
        box = BoxDefinition(width=100, height=100, length=100,weight=805,
            max_weight=19195,
            description="Carton medium",
            container_type="M",
            remark="Medium 6006380V1-00",
            max_fill_percentage=80.0,
            min_fill_percentage=5.0)
    
        # Create a layer
        layer = LayerResult(box)
    
        # Define an initial space
        initial_space_json = {
            'x': 0, 'y': 0, 'z': 0,
            'width': 100, 'height': 100, 'length': 100
        }
        initial_space = Fragment(**initial_space_json)
    
        # Define a product
        product = Product(width=50, height=50, length=50, weight=10, fit_ratio=100, item="Product1",location="06C01")
        # product.coordinates = (25, 25, 25)  # Place it in the middle of the initial space

        position = Position(product, 25, 25, 25, RotationType.initial_rotation(*(product.get_dimensions())))
    
        # Call split_space_around_product
        fragments = layer.split_space_around_product(initial_space, position)
    
        # Expected fragmented spaces
        expected_fragments_json = [
            {'x': 0, 'y': 0, 'z': 0, 'width': 25, 'height': 100, 'length': 100},  # Left of product
            {'x': 0, 'y': 0, 'z': 0, 'width': 100, 'height': 25, 'length': 100},  # Front of product
            {'x': 0, 'y': 0, 'z': 0, 'width': 100, 'height': 100, 'length': 25},  # Top of product
            {'x': 75, 'y': 0, 'z': 0, 'width': 25, 'height': 100, 'length': 100},  # Bottom of product
            {'x': 0, 'y': 75, 'z': 0, 'width': 100, 'height': 25, 'length': 100},  # Right of product
            {'x': 0, 'y': 0, 'z': 75, 'width': 100, 'height': 100, 'length': 25}  # Back of product
        ]
        expected_fragments = [Fragment(**fragment) for fragment in expected_fragments_json]
    
        # Check that all expected fragments are in the result
        for fragment in expected_fragments:
            self.assertIn(fragment, fragments, f"Fragment {fragment} is missing in the result.")
    
        # Check that there are no unexpected fragments
        for fragment in fragments:
            self.assertIn(fragment, expected_fragments, f"Unexpected fragment {fragment} found in the result.")

    def test_find_fit_in_remaining_spaces(self):
        """Test that a product can be placed in a fragmented space without collisions."""
        # Define the box and layer
        box = BoxDefinition(width=100, height=100, length=100, weight=805,
                            max_weight=19195,
                            description="Carton medium",
                            container_type="M",
                            remark="Medium 6006380V1-00",
                            max_fill_percentage=80.0,
                            min_fill_percentage=5.0)
        layer = LayerResult(box)
    
        # Define the initial remaining space
        remaining_spaces_json = [
            {'x': 0, 'y': 0, 'z': 0, 'width': 100, 'height': 100, 'length': 100}
        ]
        layer.remaining_spaces = [Fragment(**space) for space in remaining_spaces_json]
    
        # Define an already placed product (to create a fragmented space)
        existing_product = Product(width=50, height=50, length=50, weight=10, fit_ratio=100, item="ExistingProduct",location="06C01")

        position = Position(existing_product, 0, 0, 0, RotationType.initial_rotation(*(existing_product.get_dimensions())))

        layer.get_positions().append(position)
        layer.update_remaining_spaces(position)
    
        # Define a new product to fit in a fragmented space
        new_product = Product(width=25, height=25, length=25, weight=5, fit_ratio=100, item="NewProduct",location="06C01")
        existing_coordinates = layer.get_product_coordinates()  # Get coordinates of placed products
    
        # Call the method under test
        success = layer.find_fit_in_remaining_spaces(new_product, existing_coordinates)
    
        # Assertions
        self.assertTrue(success, "Product should be placed in a fragmented space.")
        self.assertIn(new_product, [position.get_product() for position in layer.get_positions()], "New product should be added to the layer's product list.")
        self.assertEqual(layer.get_positions()[-1].get_coordinates(), (50, 0, 0),
                         "Product should be placed at the correct fragmented space.")
    
        # Check that the remaining spaces were updated correctly
        remaining_space_count = len(layer.remaining_spaces)
        self.assertGreater(remaining_space_count, 0, "Remaining spaces should be updated after placing the product.")
    
        # Ensure the original fragmented spaces were modified correctly
        for space in layer.remaining_spaces:
            self.assertNotEqual(space, {'x': 0, 'y': 0, 'z': 0, 'width': 100, 'height': 100, 'length': 100},
                                "Original unfragmented space should no longer exist.")

    def test_box_packing_with_strict_bfd(self):
        logging.info("Starting test_box_packing_with_strict_bfd...")
    
        box = BoxDefinition(
            length=510,
            height=300,
            width=415,
            weight=805,
            max_weight=19195,
            description="Carton medium",
            container_type="M",
            remark="Medium 6006380V1-00",
            max_fill_percentage=80.0,
            min_fill_percentage=5.0
        )
    
        products = [
            Product(width=113, height=208, length=113, weight=900.0, fit_ratio=100, item="Product_5252",
                    location="06C01"),
            Product(width=45, height=243, length=113, weight=560.0, fit_ratio=100, item="Product_2037",
                    location="06C01"),
            Product(width=100, height=190, length=100, weight=665.0, fit_ratio=100, item="Product_5591",
                    location="06C01"),
            Product(width=138, height=210, length=138, weight=1139.0, fit_ratio=100, item="Product_3410",
                    location="06C01"),
            Product(width=100, height=120, length=100, weight=305.0, fit_ratio=100, item="Product_2026",
                    location="06C01"),
            Product(width=100, height=102, length=100, weight=282.0, fit_ratio=100, item="Product_4918",
                    location="06C01"),
            Product(width=260, height=145, length=345, weight=2518.0, fit_ratio=100, item="Product_5028",
                    location="06C01"),
        ]
    
        order = Order("TestOrder", "0", products)
        box_result = BoxResult(box)
        box_result.pack_products_by_order(order)
    
        # Expected coordinates for the products, including Starting Point and Extending Point
        # TODO: Use following data in case xyz adjustments in layer_result are 2.5,1.5,1.5
        # expected_placements = {
        #     "Product_5028": {"start": (0, 0, 0), "end": (345, 145, 260)},
        #     "Product_3410": {"start": (0, 145, 0), "end": (138, 283, 210)},
        #     "Product_5252": {"start": (0, 283, 0), "end": (208, 396, 113)},
        #     "Product_2037": {"start": (0, 283, 113), "end": (243, 396, 158)},
        #     "Product_5591": {"start": (0, 396, 0), "end": (190, 496, 100)},
        #     "Product_2026": {"start": (138, 145, 0), "end": (258, 245, 100)},
        #     "Product_4918": {"start": (258, 145, 0), "end": (360, 245, 100)},
        # }
        # TODO: Use following data in case xyz adjustments in layer_result are 2.5,2.5,2.5
        expected_placements = {
            "Product_5028": {"start": (0, 0, 0), "end": (345, 145, 260)},
            "Product_3410": {"start": (0, 145, 0), "end": (138, 283, 210)},
            "Product_5252": {"start": (138, 145, 0), "end": (346, 258, 113)},
            "Product_2037": {"start": (345, 0, 0), "end": (390, 113, 243)},
            "Product_5591": {"start": (138, 145, 113), "end": (328, 245, 213)},
            "Product_2026": {"start": (138, 245, 113), "end": (238, 345, 233)},
            "Product_4918": {"start": (238, 245, 113), "end": (340, 345, 213)},
        }

        for placement in box_result.get_products_positions():
            product_item = placement['product']
            starting_point = placement['starting_point']
            extending_point = placement['extending_point']
    
            # Extract dimensions from the placement dictionary
            dimensions = placement.get('dimensions', {})
    
            # Assert starting and extending points with detailed logging
            assert starting_point == expected_placements[product_item]["start"], (
                f"Product {product_item} has incorrect starting point: {starting_point}, "
                f"expected: {expected_placements[product_item]['start']}."
            )
    
            assert extending_point == expected_placements[product_item]["end"], (
                f"Product {product_item} has incorrect extending point: {extending_point}, "
                f"expected: {expected_placements[product_item]['end']}. "
                f"Starting point: {starting_point}, Dimensions: {dimensions}"
            )
    
        # Verify no oversized or leftover products
        self.assertEqual(box_result.get_oversized_products(), [], "No oversized products should exist.")
        self.assertEqual(box_result.get_leftover_products(), [], "All products should fit into the box.")
    
        # Log the layers and products for clarity
        logging.info(f"Layers: {len(box_result.get_layers())}")
        for idx, layer in enumerate(box_result.get_layers()):
            logging.info(f"Layer {idx + 1}: {[position.get_product().get_product_name() for position in layer.get_positions()]}")

    def test_find_fit_in_remaining_spaces_no_found_space(self):
        """Test that a product cannot be placed if no suitable space is found."""
        # Define the box and layer
        box = BoxDefinition(width=100, height=100, length=100, weight=805,
                            max_weight=19195,
                            description="Carton medium",
                            container_type="M",
                            remark="Medium 6006380V1-00",
                            max_fill_percentage=80.0,
                            min_fill_percentage=5.0)
        layer = LayerResult(box)
    
        # Define the initial remaining space
        remaining_spaces_json = [
            {'x': 0, 'y': 0, 'z': 0, 'width': 50, 'height': 50, 'length': 50}
        ]
        layer.remaining_spaces = [Fragment(**space) for space in remaining_spaces_json]
    
        # Define a new product that is too large to fit in the remaining space
        new_product = Product(width=60, height=60, length=60, weight=5, fit_ratio=100, item="NewProduct", location="06C01")
        existing_coordinates = layer.get_product_coordinates()  # Get coordinates of placed products
    
        # Call the method under test
        success = layer.find_fit_in_remaining_spaces(new_product, existing_coordinates)
    
        # Assertions
        self.assertFalse(success, "Product should not be placed as no suitable space is found.")
        self.assertNotIn(new_product, [position.get_product() for position in layer.get_positions()], "New product should not be added to the layer's product list.")
    
        # Check that the remaining spaces were not modified
        self.assertEqual(len(layer.remaining_spaces), 1, "Remaining spaces should not be modified.")
        self.assertEqual(layer.remaining_spaces[0].volume(), 50 * 50 * 50, "Remaining space volume should be unchanged.")