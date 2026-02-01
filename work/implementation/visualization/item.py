class Item:
    """
    Represents an item with a name, weight, dimensions, and position within a container.
    """

    def __init__(self, name, weight, dimension=None, position=None):
        """
        Initializes an Item object with its properties.
        
        Parameters:
        - name (str): The name or description of the item.
        - weight (float): The weight of the item.
        - dimension (list, optional): The dimensions of the item as [x, y, z]. Defaults to [0, 0, 0].
        - position (list, optional): The position of the item as [x, y, z]. Defaults to [0, 0, 0].
        """
        self.name = name
        self.weight = weight
        self._dimension = dimension if dimension else [0, 0, 0]  # Default to [0, 0, 0]
        self._position = position if position else [0, 0, 0]  # Default to [0, 0, 0]

    @property
    def dimension(self):
        """
        Retrieves the dimensions of the item.
        
        Returns:
        - list: A list representing the dimensions [x, y, z] of the item.
        """
        return self._dimension

    @dimension.setter
    def dimension(self, value):
        """
        Sets the dimensions of the item, ensuring the input is valid.
        
        Parameters:
        - value (list): A list of three numerical values representing dimensions [x, y, z].

        Raises:
        - ValueError: If the input is not a list of three numerical values.
        """
        if len(value) == 3 and all(isinstance(i, (int, float)) for i in value):
            self._dimension = value
        else:
            raise ValueError("Dimension must be a list of 3 numerical values [x, y, z].")

    @property
    def position(self):
        """
        Retrieves the position of the item.
        
        Returns:
        - list: A list representing the position [x, y, z] of the item.
        """
        return self._position

    @position.setter
    def position(self, value):
        """
        Sets the position of the item, ensuring the input is valid.
        
        Parameters:
        - value (list): A list of three numerical values representing position [x, y, z].

        Raises:
        - ValueError: If the input is not a list of three numerical values.
        """
        if len(value) == 3 and all(isinstance(i, (int, float)) for i in value):
            self._position = value
        else:
            raise ValueError("Position must be a list of 3 numerical values [x, y, z].")

    def __repr__(self):
        """
        Provides a string representation of the Item object.
        
        Returns:
        - str: A string describing the item, including its name, weight, dimensions, and position.
        """
        return f"Item(name={self.name}, weight={self.weight}, dimension={self.dimension}, position={self.position})"
