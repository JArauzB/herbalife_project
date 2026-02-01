import logging

from .rotation_type import RotationType

class Position:
    """
    Represents the position and orientation of a product within a box in 3D space.
    This class is fundamental to the packing algorithm as it handles all aspects of
    product placement and rotation.

    The coordinate system used is:
    - Origin (0,0,0) at the bottom-left-front corner of the box
    - X axis: width (left to right)
    - Y axis: height (bottom to top) 
    - Z axis: length (front to back)

    Attributes:
        product (Product): The product being positioned
        location_x (float): X coordinate in cm from left wall
        location_y (float): Y coordinate in cm from bottom
        location_z (float): Z coordinate in cm from front
        rotation (RotationType): Current rotation state of the product
        rotated_width (float): Width after applying rotation
        rotated_height (float): Height after applying rotation
        rotated_length (float): Length after applying rotation
        coordinates (tuple): Cached (x,y,z) coordinates for performance

    The Position class works closely with:
    - LayerResult: For layer-based packing
    - RotationType: For product orientation
    - BoxResult: For final placement validation
    """

    def __init__(self, product, location_x, location_y, location_z, rotation):
        """
        Initializes a Position object with specific coordinates and rotation.

        Args:
            product (Product): The product to position
            location_x (float): Distance in cm from left wall
            location_y (float): Distance in cm from bottom
            location_z (float): Distance in cm from front
            rotation (RotationType): Initial rotation state

        Note:
            Rotated dimensions are calculated and cached immediately for performance.
            The coordinates tuple is also cached to avoid repeated creation.
        """
        self.product = product
        self.location_x = location_x
        self.location_y = location_y
        self.location_z = location_z
        self.rotation = rotation

        # Compute rotated dimensions
        self.rotated_width, self.rotated_height, self.rotated_length = rotation.adjust_dimensions(
            product.width, product.height, product.length
        )

        # Set initial coordinates
        self.coordinates = (location_x, location_y, location_z)
        logging.debug(f"[DEBUG] Initializing Position with product: {product}, location_x: 0, location_y: 0, location_z: 0")

    def calculate_extending_point(self):
        """
        Calculates the far corner coordinates of the product's bounding box.
        This is essential for collision detection and space utilization checks.

        Returns:
            tuple: (x2, y2, z2) coordinates of the opposite corner in cm

        Note:
            The extending point represents the maximum extent of the product
            in each dimension after applying the current rotation.
        """
        return tuple(a + b for a, b in zip(self.get_coordinates(), self.get_dimensions()))

    def copy(self):
        """
        Creates a deep copy of this position instance.
        Used when evaluating different placement possibilities during packing.

        Returns:
            Position: New position instance with identical attributes

        Note:
            Essential for testing different product placements without
            modifying the original position.
        """
        return Position(self.product, self.location_x, self.location_y, self.location_z, self.rotation)

    def __eq__(self, other):
        """
        Compares two Position objects for equality.
        Positions are equal if they have the same product, coordinates, and rotation.

        Args:
            other (Position): Another Position object to compare with

        Returns:
            bool: True if positions are equivalent, False otherwise
        """
        return self.product == other.product and self.coordinates == other.coordinates and self.rotation == other.rotation


    def get_product(self):
        """
        Retrieves the product associated with this position.

        Returns:
            Product: The product being positioned

        Note:
            Used frequently by the packing algorithm to access product properties
            and validate placements.
        """
        return self.product
    
    def get_coordinates(self):
        """
        Returns the current position coordinates.
        Uses cached coordinates for performance optimization.

        Returns:
            tuple: (x, y, z) coordinates in cm from the box origin

        Note:
            These coordinates represent the bottom-left-front corner of the product.
        """
        return self.coordinates

    def get_rotation(self):
        """
        Returns the current rotation state of the product.

        Returns:
            RotationType: Current rotation configuration

        Note:
            Used for dimension calculations and placement validation.
        """
        return self.rotation
    
    def get_dimensions(self):
        """
        Returns the product's dimensions after applying the current rotation.

        Returns:
            tuple: (width, height, length) in cm after rotation

        Note:
            Critical for space calculations and collision detection.
            Uses the RotationType to calculate the actual dimensions.
        """
        return self.rotation.adjust_dimensions(*(self.product.get_dimensions()))


    def set_orientation(self, rotation):
        """
        Updates the product's rotation and recalculates dimensions.
        
        Args:
            rotation (RotationType): New rotation to apply

        Note:
            - Updates internal rotation state
            - Recalculates rotated dimensions
            - Used during packing optimization
            - Logs changes for debugging purposes
        """
        self.rotation = rotation

        # Recalculate rotated dimensions based on the new rotation
        self.rotated_width, self.rotated_height, self.rotated_length = rotation.adjust_dimensions(
            self.product.width, self.product.height, self.product.length
        )

        # Log the new orientation and rotated dimensions
        logging.debug(f"Set new orientation for product {self.product.item}. Rotation: {rotation.name}, "
                      f"New rotated dimensions: {self.rotated_width}x{self.rotated_height}x{self.rotated_length}")

    def set_coordinates(self, x, y, z):
        """
        Updates the position coordinates of the product.
        
        Args:
            x (float): New X coordinate in cm
            y (float): New Y coordinate in cm
            z (float): New Z coordinate in cm

        Note:
            - Updates both individual coordinates and cached tuple
            - Represents bottom-left-front corner of product
            - Used during product placement optimization
            - Changes are logged for debugging
        """
        self.location_x = x
        self.location_y = y
        self.location_z = z

        # Update the coordinates tuple to reflect the new location
        self.coordinates = (x, y, z)

        # Log the updated coordinates
        logging.debug(f"Updated coordinates for product {self.product.item}: "
                      f"({x}, {y}, {z})")
