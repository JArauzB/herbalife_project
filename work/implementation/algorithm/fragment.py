class Fragment:
    """
    Represents a free space fragment within a packing layer.
    This class is crucial for space management in the bin packing algorithm,
    tracking and managing available spaces after product placement.

    The fragment system works by:
    - Representing empty spaces in 3D
    - Tracking spaces created when products are placed
    - Managing space splitting and merging
    - Optimizing space utilization

    Attributes:
        x (float): X-coordinate of fragment's origin in cm (from left)
        y (float): Y-coordinate of fragment's origin in cm (from bottom)
        z (float): Z-coordinate of fragment's origin in cm (from front)
        width (float): Width of the fragment in cm (X dimension)
        height (float): Height of the fragment in cm (Y dimension)
        length (float): Length of the fragment in cm (Z dimension)
        new (bool): Flag indicating if this is a newly created fragment

    Key Concepts:
        - Fragments are created when products are placed
        - Each fragment represents a potential space for new products
        - Fragments can be split to accommodate new products
        - Fragment dimensions must be positive
        - Fragments track their creation status for optimization
    """

    def __init__(self, x, y, z, width, height, length):
        """
        Creates a new space fragment with specified dimensions and position.
        
        Args:
            x (float): Distance from left wall in cm
            y (float): Distance from bottom in cm
            z (float): Distance from front in cm
            width (float): Fragment width in cm
            height (float): Fragment height in cm
            length (float): Fragment length in cm

        Note:
            - All dimensions must be positive
            - New fragments are marked with new=True
            - Coordinates represent the bottom-left-front corner
            - Used by LayerResult for space management
        """
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.length = length
        self.new = True

    def volume(self):
        """
        Calculates the volume of the fragment.
        Used for space utilization calculations and optimization.
        
        Returns:
            float: Volume of the fragment in cubic centimeters

        Note:
            - Critical for determining if products can fit
            - Used in space optimization algorithms
            - Helps track packing efficiency
        """
        return self.width * self.height * self.length

    def __repr__(self):
        """
        Provides a string representation of the fragment.
        Useful for debugging and logging placement operations.
        
        Returns:
            str: Human-readable representation of fragment position and dimensions

        Format:
            Fragment(x=X, y=Y, z=Z, width=W, height=H, length=L)
        """
        return f"Fragment(x={self.x}, y={self.y}, z={self.z}, width={self.width}, height={self.height}, length={self.length})"

    def __eq__(self, other):
        """
        Compares two fragments for equality.
        Fragments are equal if they have identical positions and dimensions.
        
        Args:
            other (Fragment): Another fragment to compare with

        Returns:
            bool: True if fragments are identical, False otherwise

        Note:
            - Used in fragment management and merging
            - Considers all dimensions and coordinates
            - Ignores the 'new' status flag
        """
        if isinstance(other, Fragment):
            return (self.x == other.x and self.y == other.y and self.z == other.z and
                    self.width == other.width and self.height == other.height and self.length == other.length)

        return False