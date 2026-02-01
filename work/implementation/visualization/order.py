class Order:
    """
    Represents an order containing multiple boxes.
    """

    def __init__(self, order_id):
        """
        Initializes an Order object with its unique ID and an empty list of boxes.
        
        Parameters:
        - order_id (str or int): The unique identifier for the order.
        """
        self.order_id = order_id
        self.boxes = []  # List to store Box objects

    def add_box(self, box):
        """
        Adds a Box object to the order.

        Parameters:
        - box (Box): The Box object to add to the order.
        """
        self.boxes.append(box)

    def get_order_id(self):
        """
        Retrieves the unique ID of the order.

        Returns:
        - str or int: The unique identifier for the order.
        """
        return self.order_id

    def get_boxes(self):
        """
        Retrieves the list of boxes associated with the order.

        Returns:
        - list: A list of Box objects in the order.
        """
        return self.boxes

    def count_boxes(self):
        """
        Counts the number of boxes in the order.

        Returns:
        - int: The number of boxes in the order.
        """
        return len(self.boxes)

    def __repr__(self):
        """
        Provides a string representation of the Order object.

        Returns:
        - str: A string describing the order, including its ID and associated boxes.
        """
        return f"Order(id={self.order_id}, boxes={self.boxes})"


