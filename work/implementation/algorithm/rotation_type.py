from enum import Enum, auto

class RotationType(Enum):
    """
    Defines all possible 3D rotations of a product in a box using an enumeration.
    This class is crucial for the bin packing algorithm as it handles all possible
    ways a product can be oriented in 3D space.

    The rotation system defines 6 unique orientations:
    RT1: Original orientation (w, h, l)
    RT2: Rotated 90° around Y (l, h, w)
    RT3: Original width as height (h, w, l)
    RT4: Rotated 90° around Y with height swap (l, w, h)
    RT5: Original height as depth (h, l, w)
    RT6: Original width as depth (w, l, h)

    Key Concepts:
        - Each rotation represents a unique orientation in 3D space
        - Rotations maintain right-handed coordinate system
        - Dimensions are adjusted according to rotation type
        - Rotations can be cycled through sequentially

    Usage:
        Used by the packing algorithm to:
        - Try different product orientations
        - Find optimal product placement
        - Maximize space utilization
        - Ensure stable product positioning
    """

    RT1 = auto()  # w, h, l - Original orientation
    RT2 = auto()  # l, h, w - 90° Y rotation
    RT3 = auto()  # h, w, l - Width as height
    RT4 = auto()  # l, w, h - 90° Y + height swap
    RT5 = auto()  # h, l, w - Height as depth
    RT6 = auto()  # w, l, h - Width as depth

    @staticmethod
    def initial_rotation(w, h, l):
        """
        Determines the optimal initial rotation for given dimensions.
        This method analyzes the product dimensions to find the most
        stable starting orientation.

        Args:
            w (float): Original width in cm
            h (float): Original height in cm
            l (float): Original length in cm

        Returns:
            RotationType: Most suitable initial rotation

        Note:
            - Prioritizes larger base area for stability
            - Considers natural product orientation
            - Helps optimize subsequent rotation attempts
        """
        dimensions = [(w, h, l), (l, h, w), (h, w, l), (l, w, h), (h, l, w), (w, l, h)]
        sorted_dimensions = sorted([w, h, l])
        altered_dimensions = (sorted_dimensions[1], sorted_dimensions[0], sorted_dimensions[2])
        index = dimensions.index(altered_dimensions)
        return RotationType(index + RotationType.min_value())

    def adjust_dimensions(self, w, h, l):
        """
        Calculates new dimensions after applying this rotation.
        
        Args:
            w (float): Original width in cm
            h (float): Original height in cm
            l (float): Original length in cm

        Returns:
            tuple: (new_width, new_height, new_length) in cm

        Note:
            - Maintains dimensional integrity
            - Critical for space calculations
            - Used in collision detection
        """
        if self == RotationType.RT1:
            return w, h, l  # Original orientation
        elif self == RotationType.RT2:
            return l, h, w  # 90° Y rotation
        elif self == RotationType.RT3:
            return h, w, l  # Width as height
        elif self == RotationType.RT4:
            return l, w, h  # 90° Y + height swap
        elif self == RotationType.RT5:
            return h, l, w  # Height as depth
        elif self == RotationType.RT6:
            return w, l, h  # Width as depth

    def next_rotation(self):
        """
        Advances to the next rotation in sequence.
        Used to systematically try different orientations.

        Returns:
            RotationType: Next rotation in sequence

        Note:
            Cycles through all possible rotations
        """
        new_value = (self.value) % RotationType.max_value()
        return RotationType(new_value + RotationType.min_value())

    def previous_rotation(self):
        """
        Moves to the previous rotation type and returns the updated RotationType.

        Returns:
            (RotationType): The updated rotation type.
        """
        new_value = (self.value + RotationType.max_value() - RotationType.min_value() - 1) % RotationType.max_value()

        return RotationType(new_value + 1)
    
    @staticmethod
    def min_value():
        """
        Returns the minimum value of the RotationType enumeration.

        Returns:
            (int): The minimum value of the RotationType enumeration.
        """
        return RotationType.RT1.value
    
    @staticmethod
    def max_value():
        """
        Returns the maximum value of the RotationType enumeration.

        Returns:
            (int): The maximum value of the RotationType enumeration.
        """
        return RotationType.RT6.value