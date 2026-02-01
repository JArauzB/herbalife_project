import logging

from .order import Order
from .rotation_type import RotationType
from .box_definition import BoxDefinition
from .layer_result import LayerResult
from .position import Position

class BoxResult:
    """
    Represents the result of packing products into a specific box.
    This class manages the layer-based packing results and tracks product placement
    within a single box instance.

    The packing system uses a layer-based approach where:
    - Products are packed in horizontal layers
    - Each layer is managed by a LayerResult instance
    - Products that don't fit are tracked separately
    - Unique box IDs are generated for tracking

    Attributes:
        box (BoxDefinition): The box being packed
        layers (List[LayerResult]): Horizontal layers of packed products
        oversized_products (List[Product]): Products too large for the box
        leftover_products (List[Product]): Products that couldn't be placed
        box_id (int): Unique identifier for this box instance
        order (Order): Associated order being packed
        packed_items (List[Product]): Successfully packed products

    Key Features:
        - Layer-based packing strategy
        - Oversized product detection
        - Space optimization
        - Position tracking
        - Pack validation
    """

    def __init__(self, box: BoxDefinition):
        """
        Initializes a new box packing result.

        Args:
            box (BoxDefinition): The box definition to use for packing

        Note:
            - Generates a unique box ID using Python's id() function
            - Initializes empty lists for layers and unplaced products
            - Sets up tracking for the packing process
        """
        self.box = box
        self.layers = []  # Each layer contains its products and dimensions
        self.oversized_products = []  # Products too large to fit in the box
        self.leftover_products = []  # Products that couldn't fit despite trying
        self.box_id = id(self)  # Generate a unique ID for the box instance



    def pack_products_by_order(self, order: Order):
        """
        Packs products from an order into this box using a layer-based approach.
        
        The packing process:
        1. Orders items for optimal packing
        2. Attempts to place each product
        3. Tracks rejected items
        4. Manages layer creation and utilization

        Args:
            order (Order): The order containing products to pack

        Note:
            - Products are packed sequentially
            - Failed placements are tracked as rejected items
            - Logging is used to track packing progress
        """
        self.order = order
        self.order.order_items()

        while True:
            product = self.order.take_item()

            if not product:
                break

            if not self.add_product_to_box(product):
                logging.warning(f"Product {product.get_product_name()} could not be packed into the box.")
                self.order.add_rejected_item(product)

    def product_is_oversized(self, product):
        """
        Determines if a product is too large for this box.
        
        Checks all dimensions of the product against the box dimensions,
        considering all possible rotations.

        Args:
            product (Product): Product to check

        Returns:
            bool: True if product is too large for the box, False otherwise

        Note:
            Products marked as oversized are tracked separately and won't
            be attempted for packing
        """
        return any(dim > max_dim for dim, max_dim in zip(sorted(product.get_dimensions()), sorted(self.box.get_box_dimensions())))

    def add_product_to_box(self, product):
        """
        Attempts to add a product to the box using the layer-based packing strategy.
        
        The placement algorithm:
        1. Checks if product is oversized
        2. Attempts placement in existing layers
        3. Creates new layer if necessary
        4. Updates tracking for successful/failed placements

        Args:
            product (Product): Product to place in the box

        Returns:
            bool: True if product was successfully placed, False otherwise

        Note:
            - Considers all possible rotations
            - Optimizes for space utilization
            - Maintains stability through proper support
        """
        if self.product_is_oversized(product):
            self.oversized_products.append(product)
            logging.warning(f"Product {product.item} is too large to fit in the box.")
            return False

        existing_coordinates = self.collect_existing_coordinates()

        # Wrap product in a Position object
        rotation = RotationType.initial_rotation(product.width, product.height, product.length)
        position = Position(product, 0, 0, 0, rotation)

        logging.debug(f"Position for product {product.item}: {position}, Coordinates: {position.get_coordinates()}")

        # Try to place the product in existing layers
        for idx, layer in enumerate(self.layers):
            logging.debug(f"Attempting to place product {position.get_product().item} in Layer {idx + 1}.")
            if layer.add_product(position, existing_coordinates):
                logging.debug(f"Product {product.item} successfully placed in Layer {idx + 1}.")
                return True

        # If no existing layer fits, create a new layer
        if self.add_new_layer(position, existing_coordinates):
            logging.debug(f"Product {product.item} successfully added to a new layer.")
            return True

        # Mark the product as leftover if no fit
        self.leftover_products.append(product)
        logging.warning(f"Product {product.item} could not be placed in any layer.")
        return False

    def add_new_layer(self, position, existing_coordinates):
        """
        Creates and initializes a new packing layer in the box.
        
        Args:
            position (Position): Initial product position for the layer
            existing_coordinates (List[tuple]): Coordinates of already placed products

        Returns:
            bool: True if layer was created and product placed, False otherwise

        Note:
            - Checks remaining vertical space
            - Initializes layer at correct height
            - Attempts initial product placement
            - Logs layer creation process
        """
        if position.get_coordinates() is None:
            logging.error(f"Position for product {position.get_product().item} has invalid coordinates.")
            raise ValueError(f"Invalid coordinates for product {position.get_product().item}.")

        new_layer_base_height = sum(layer.layer_height for layer in self.layers)
        remaining_height = self.box.height - new_layer_base_height

        if remaining_height >= min(position.product.get_dimensions()):
            new_layer = LayerResult(self.box, base_height=new_layer_base_height)
            logging.debug(f"Attempting to add new layer for product {position.get_product().item}.")
            logging.debug(f"Position details: {position}, Coordinates: {position.get_coordinates()}")

            if new_layer.add_product(position, existing_coordinates):
                self.layers.append(new_layer)
                logging.debug(f"Product {position.get_product().item} packed into a new layer.")
                return True

        logging.warning(
            f"Product {position.get_product().item} cannot fit in a new layer. "
            f"Remaining height: {remaining_height}, Product height: {position.product.height}."
        )
        return False

    def collect_existing_coordinates(self):
        """
        Collects coordinates of all products currently placed in the box.
        Used for collision detection and space management.

        Returns:
            List[tuple]: List of (product_id, x, y, z, width, height, length)
                        for each placed product

        Note:
            Coordinates are collected from all layers for complete
            collision detection
        """
        existing_coordinates = []
        for layer in self.layers:
            existing_coordinates.extend(layer.get_product_coordinates())
        return existing_coordinates

    def get_all_coordinates(self):
        """Get all product coordinates for tracking."""
        all_coordinates = []
        for layer in self.layers:
            all_coordinates.extend(layer.get_positions())
        return all_coordinates

    def get_oversized_products(self):
        """
        Returns a list of products that are too large to fit into the box.

        Returns:
            (List[Product]): A list of products that are too large to fit into the box.
        """
        return self.oversized_products

    def get_leftover_products(self):
        """
        Returns a list of products that could not be placed into any layer.

        Returns:
            (List[Product]): A list of products that could not be placed into any layer.
        """
        return self.leftover_products

    def get_products_positions(self):
        """
        Retrieves detailed position information for all packed products.
        
        Returns:
            List[Dict]: List of dictionaries containing:
                - Product information
                - Starting coordinates
                - Extending point coordinates
                - Rotation information
                - Dimensions after rotation

        Note:
            Used for visualization and validation of packing results
        """
        products_positions = []
        try:
            logging.debug(f"Starting to retrieve product positions...")
            logging.debug(f"Processing {len(self.layers)} layers.")

            for layer_index, layer in enumerate(self.layers):
                logging.debug(f"Processing Layer {layer_index + 1} with {len(layer.get_positions())} products.")
                for position in layer.get_positions():  # Ensure `get_products` returns Position objects
                    start_x, start_y, start_z = position.get_coordinates()
                    end_x, end_y, end_z = position.calculate_extending_point()

                    products_positions.append({
                        'product': position.get_product().item,  # Access the product's item name
                        'starting_point': (start_x, start_y, start_z),
                        'extending_point': (end_x, end_y, end_z),
                        'rotated_dimensions': (
                            position.get_dimensions()
                        ),
                        'rotation': position.get_rotation().name,
                    })

            logging.debug(f"Successfully retrieved product positions.")
            return products_positions

        except Exception as e:
            logging.error(f"An error occurred while retrieving product positions: {e}")
            raise e  # Reraise the exception to handle it elsewhere if needed

    def get_box_id(self):
        """
        Returns the unique ID of the box.

        Returns:
            (int): The unique ID of the box.
        """
        return self.box_id

    def get_box_definition(self):
        """
        Returns the box definition associated with this BoxResult.

        Returns:
            (BoxDefinition): The definition of the box.
        """
        return self.box

    def get_layers(self):
        """
        Returns the layers in the box.

        Returns:
            (List[LayerResult]): The layers in the box.
        """
        return self.layers