class Item:
    def __init__(self, name, weight, dimension=None, position=None):
        self.name = name
        self.weight = weight
        # Set default values for dimension and position if not provided
        self._dimension = dimension if dimension else [0, 0, 0]  # [x, y, z]
        self._position = position if position else [0, 0, 0]  # [x, y, z]

    def __repr__(self):
        return (f"Item(name={self.name}, weight={self.weight}, "
                f"dimension={self._dimension}, position={self._position})")

    # Getters and setters for dimension
    @property
    def dimension(self):
        return self._dimension

    @dimension.setter
    def dimension(self, value):
        if len(value) == 3 and all(isinstance(i, (int, float)) for i in value):
            self._dimension = value
        else:
            raise ValueError("Dimension must be a list of 3 numerical values [x, y, z].")

    # Getters and setters for position
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if len(value) == 3 and all(isinstance(i, (int, float)) for i in value):
            self._position = value
        else:
            raise ValueError("Position must be a list of 3 numerical values [x, y, z].")