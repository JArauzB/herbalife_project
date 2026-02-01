class BoxDefinition:
    """
    Represents a box with dimensions, weight, and additional attributes for packaging calculations.
    This class is fundamental to the packing algorithm as it defines the constraints and properties
    of containers that can hold products.

    The box dimensions are automatically sorted in the constructor so that:
    - height is always the largest dimension
    - width is the second largest
    - length is the smallest dimension
    This standardization helps with consistent rotation and fitting calculations.

    Attributes:
        width (float): The width of the box in centimeters (second largest dimension)
        height (float): The height of the box in centimeters (largest dimension)
        length (float): The length of the box in centimeters (smallest dimension)
        weight (float): The empty weight of the box in grams
        max_weight (float): The maximum total weight the box can hold in grams (including box weight)
        description (str): Human-readable description of the box
        container_type (str): Classification/type of the container (e.g., "Cardboard", "Plastic")
        remark (str): Additional notes or special handling instructions
        max_fill_percentage (float): Maximum volume utilization allowed (0-100)
        min_fill_percentage (float): Minimum volume utilization required (0-100)

    Methods:
        fits_within(product_volume, product_weight) -> bool:
            Determines if a product can fit in the box based on volume and weight constraints.
        fits_with_dimensions(product_dimensions) -> bool:
            Checks if a product's physical dimensions can fit within the box in any rotation.
        min_volume() -> float:
            Calculates the minimum required product volume based on min_fill_percentage.
        max_volume() -> float:
            Calculates the maximum allowed product volume based on max_fill_percentage.
        get_box_type() -> str:
            Retrieves the container classification.
        get_box_dimensions() -> tuple:
            Returns the standardized dimensions (width, height, length).
    """

    def __init__(self, length: float, height: float, width: float, weight: float, 
                 max_weight: float, description: str, container_type: str, remark: str, 
                 max_fill_percentage: float, min_fill_percentage: float):
        """
        Initializes a Box object with the given specifications.
        The dimensions are automatically sorted to maintain consistent orientation.

        Args:
            length (float): The length of the box in cm (will be set as smallest dimension)
            height (float): The height of the box in cm (will be set as largest dimension)
            width (float): The width of the box in cm (will be set as second largest)
            weight (float): The empty weight of the box in grams
            max_weight (float): Maximum weight capacity in grams (including box weight)
            description (str): Human-readable description
            container_type (str): Type/classification of the container
            remark (str): Additional notes or instructions
            max_fill_percentage (float): Maximum volume utilization (0-100)
            min_fill_percentage (float): Minimum volume utilization (0-100)

        Note:
            The constructor automatically reorganizes dimensions to maintain:
            height >= width >= length
            This standardization is crucial for consistent rotation calculations.
        """
        self.length = length
        self.height = height
        self.width = width
        self.weight = weight
        self.max_weight = max_weight
        self.description = description
        self.container_type = container_type
        self.remark = remark
        self.max_fill_percentage = max_fill_percentage
        self.min_fill_percentage = min_fill_percentage

        if self.height > self.width:
            self.height, self.width = self.width, self.height
        if self.height < self.length:
            self.height, self.length = self.length, self.height
        if self.height < self.width:
            self.height, self.width = self.width, self.height
    
    def fits_within(self, product_volume: float, product_weight: float):
        """
        Determines if a product can fit within the box based on volume and weight constraints.
        Considers both the minimum and maximum fill percentages, as well as weight limitations.

        Args:
            product_volume (float): The volume of the product in cubic centimeters
            product_weight (float): The weight of the product in grams

        Returns:
            bool: True if the product fits within all constraints (volume and weight),
                 False otherwise

        Note:
            The weight check includes subtracting the box's own weight from max_weight
            to ensure the total weight (box + contents) doesn't exceed max_weight.
        """
        return self.min_volume() <= product_volume <= self.max_volume() and product_weight <= (self.max_weight - self.weight)

    def fits_with_dimensions(self, product_dimensions: tuple):
        """
        Checks if a product's physical dimensions can fit within the box in any rotation.
        Compares the sorted dimensions of the product against the sorted dimensions of the box.

        Args:
            product_dimensions (tuple): The dimensions (length, width, height) of the product in cm

        Returns:
            bool: True if the product can fit in at least one orientation,
                 False if the product is too large in any dimension

        Note:
            Both the product and box dimensions are sorted in descending order before comparison,
            ensuring that the largest product dimension is compared against the largest box
            dimension, and so on.
        """
        return all(dim <= max_dim for dim, max_dim in zip(sorted(product_dimensions, reverse=True), sorted((self.width, self.height, self.length), reverse=True)))
    
    def min_volume(self):
        """
        Calculates the minimum required volume of products based on min_fill_percentage.
        This helps ensure efficient use of box space and prevents under-filling.

        Returns:
            float: The minimum volume of product contents in cubic centimeters

        Note:
            The calculation uses the min_fill_percentage to determine the smallest
            acceptable volume of products that should be packed into this box.
        """
        return ((self.width * self.height * self.length) * self.min_fill_percentage) / 100
    
    def max_volume(self):
        """
        Calculates the maximum allowed volume of products based on max_fill_percentage.
        This helps prevent over-filling and potential damage to contents.

        Returns:
            float: The maximum volume of product contents in cubic centimeters

        Note:
            The calculation uses the max_fill_percentage to determine the largest
            acceptable volume of products that can be safely packed into this box.
        """
        return ((self.width * self.height * self.length) * self.max_fill_percentage) / 100
    
    def get_box_type(self):
        """
        Retrieves the container classification.

        Returns:
            str: The type of the container
        """
        return self.container_type
    
    def get_box_dimensions(self):
        """
        Returns the standardized dimensions (width, height, length).

        Returns:
            tuple: The dimensions of the box (width, height, length)
        """
        return self.width, self.height, self.length
        