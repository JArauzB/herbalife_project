class Box:
    """
    Represents a container (box) that holds items and has specific dimensions.
    """

    def __init__(self, box_id, dimension=None, box_name=""):
        """
        Initializes a Box object with a unique ID, optional dimensions, and a name.
        
        Parameters:
        - box_id (int): Unique identifier for the box.
        - dimension (list, optional): Dimensions of the box as [x, y, z]. Defaults to [0, 0, 0].
        - box_name (str, optional): A descriptive name for the box. Defaults to an empty string.
        """
        self.box_id = box_id
        self.box_name = box_name
        self._dimension = dimension if dimension else [0, 0, 0]  # [x, y, z]
        self.items = []  # List to hold Item objects

    def add_item(self, item):
        """
        Adds an item to the box.
        
        Parameters:
        - item (Item): An instance of an item to be added to the box.
        """
        self.items.append(item)

    def get_box_id(self):
        """
        Retrieves the unique identifier of the box.
        
        Returns:
        - int: The unique box ID.
        """
        return self.box_id

    def get_box_name(self):
        """
        Retrieves the name of the box.
        
        Returns:
        - str: The name of the box.
        """
        return self.box_name

    def get_dimentions(self):
        """
        Retrieves the dimensions of the box.
        
        Returns:
        - list: A list containing the dimensions [x, y, z] of the box.
        """
        return self._dimension

    def get_items(self):
        """
        Retrieves the items stored in the box.
        
        Returns:
        - list: A list of Item objects contained in the box.
        """
        return self.items

    def count_items(self):
        """
        Counts the number of items in the box.
        
        Returns:
        - int: The number of items stored in the box.
        """
        return len(self.items)

    def __repr__(self):
        """
        Provides a string representation of the Box object.
        
        Returns:
        - str: A string describing the box, including its ID and contained items.
        """
        return f"Box(id={self.box_id}, items={self.items})"

    def get_full_dimensions(self):
        """Returns box dimensions as a tuple (length, width, height)."""
        return tuple(self._dimension)