from .rotation_type import RotationType


class Product:
    """
    Represents a physical product to be packed, with its dimensions and properties.
    This class is fundamental to the packing algorithm as it defines the items
    that need to be placed in boxes.

    The product model uses:
    - Three-dimensional measurements (width, height, length)
    - Weight specifications
    - Fit ratio for volume calculations
    - Location tracking for picking
    - Unique item identification

    Attributes:
        width (float): Product width in centimeters
        height (float): Product height in centimeters
        length (float): Product length in centimeters
        weight (float): Product weight in grams
        fit_ratio (float): Volume utilization factor (0-100%)
        item (str): Unique product identifier
        location (str): Product's picking location

    Key Features:
        - Volume calculations with fit ratio
        - Dimension comparison
        - Product identification
        - Location tracking
        - Weight management
    """

    def __init__(self, width: float, height: float, length: float, weight: float, 
                 fit_ratio: float, item: str, location: str):
        """
        Initializes a product with its physical properties and metadata.

        Args:
            width (float): Product width in cm
            height (float): Product height in cm
            length (float): Product length in cm
            weight (float): Product weight in grams
            fit_ratio (float): Volume utilization percentage (0-100)
            item (str): Product identifier
            location (str): Picking location reference

        Note:
            - All dimensions must be positive
            - Fit ratio affects volume calculations
            - Location used for picking optimization
        """
        self.width = width
        self.height = height
        self.length = length
        self.weight = weight
        self.fit_ratio = fit_ratio
        self.item = item
        self.location = location

    
    def volume(self):
        """
        Calculates the effective volume of the product considering fit ratio.
        Critical for box space utilization calculations.

        Returns:
            float: Effective volume in cubic centimeters

        Note:
            - Includes fit ratio adjustment
            - Used for packing optimization
            - Critical for box selection
        """
        return self.width * self.height * self.length * (self.fit_ratio / 100)


    def __lt__(self, other):
        """
        Compares products for sorting optimization.
        Used to determine packing order.

        Args:
            other (Product): Product to compare against

        Returns:
            bool: True if this product should be packed before other

        Note:
            - Considers total dimensions
            - Factors in volume
            - Uses weight as tiebreaker
            - Critical for packing efficiency
        """
        if self.item == other.item:
            return False

        self_value = sum(self.get_dimensions())
        other_value = sum(other.get_dimensions())
        if self_value != other_value:
            return self_value < other_value

        if self.volume() != other.volume():
            return self.volume() < other.volume()
        
        # Compare by weight
        if self.weight != other.weight:
            return self.weight < other.weight

        # If all checks fail, the products are considered equal
        return False

    def get_product_name(self):
        """
        Retrieves the product's unique identifier.
        Used for tracking and reporting.

        Returns:
            str: Product identifier

        Note:
            - Used in packing results
            - Links to external systems
            - Identifies products in output
        """
        return self.item
    
    def get_dimensions(self):
        """
        Returns the product's physical dimensions.
        Used for rotation and fitting calculations.

        Returns:
            tuple: (width, height, length) in centimeters

        Note:
            - Used for rotation calculations
            - Critical for fit checking
            - Maintains dimension order
        """
        return self.width, self.height, self.length