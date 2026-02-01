from .product import Product

class Order:
    """
    Represents a customer order in the packing system.
    This class manages the products to be packed and their processing state.

    The order system manages:
    - Product lists (pending, taken, rejected, packed)
    - Order metadata (number, date)
    - Product sorting and prioritization
    - Order state tracking

    Attributes:
        rejected_items (List[Product]): Products that couldn't be packed
        items (List[Product]): Products pending packing
        taken_items (List[Product]): Products currently being processed
        packed_items (List[Product]): Successfully packed products
        order_number (str): Unique identifier for the order
        date_time (str): Order timestamp

    Key Features:
        - Product state management
        - Volume and weight calculations
        - Dimension analysis
        - Product sorting optimization
        - Order reset capabilities
        - Item tracking through packing process
    """
    
    def __init__(self, order_number, date_time, items = []):
        """
        Initializes a new order with metadata and optional initial items.

        Args:
            order_number (str): Unique order identifier
            date_time (str): Order timestamp
            items (List[Product], optional): Initial products to add

        Note:
            - Initializes all product tracking lists
            - Sets order metadata
            - Prepares for product management
        """
        self.order_number = order_number
        self.date_time = date_time
        self.rejected_items = []
        self.items = items
        self.taken_items = []
        self.packed_items = []
    
    def add_item(self, item):
        """
        Adds a single product to the order.
        Used for individual product additions.

        Args:
            item (Product): Product to add to the order

        Note:
            - Adds to pending items list
            - Used during order building
            - Maintains product state
        """
        self.items.append(item)
    
    def add_items(self, items):
        """
        Adds multiple products to the order at once.
        Optimizes products for packing after addition.

        Args:
            items (List[Product]): Products to add to the order

        Note:
            - Extends pending items list
            - Triggers product sorting
            - Prepares for packing
        """
        self.items.extend(items)

        self.order_items()
    
    def add_rejected_item(self, item):
        """
        Marks a product as rejected from packing.
        Manages product state transitions.

        Args:
            item (Product): Product that couldn't be packed

        Note:
            - Moves product to rejected list
            - Removes from pending/taken lists
            - Tracks packing failures
        """
        self.rejected_items.append(item)

        if item in self.items:
            self.items.remove(item)
        
        if item in self.taken_items:
            self.taken_items.remove(item)

    
    def reset_rejected_items(self):
        """
        Returns rejected items to pending status.
        Used when retrying packing with different parameters.

        Note:
            - Moves items back to pending list
            - Clears rejected items list
            - Triggers product resorting
            - Enables packing retries
        """
        self.items.extend(self.rejected_items)
        self.rejected_items = []
        
        self.order_items()
    
    def reset_all_items(self):
        """
        Resets all items to pending status.
        Used for complete packing restart.

        Note:
            - Consolidates all items to pending list
            - Clears other product lists
            - Resets packing progress
            - Triggers product resorting
        """
        self.items.extend(self.rejected_items)
        self.rejected_items = []
        self.items.extend(self.taken_items)
        self.taken_items = []

        self.order_items()
    
    def order_items(self):
        """
        Sorts products for optimal packing sequence.
        Critical for efficient space utilization.

        Note:
            - Sorts by volume and dimensions
            - Optimizes packing efficiency
            - Considers product stability
            - Affects packing success rate
        """
        self.items = sorted(self.items, key=lambda item: item, reverse=True)
    
    def get_items(self):
        """
        Returns the list of items in the order.

        Returns:
            (list): The list of items in the order.
        """
        templist = self.items
        self.taken_items.extend(templist)
        self.items = []

        return templist
    
    def get_total_volume(self):
        """
        Calculates total volume of all pending products.
        Used for box selection and capacity planning.

        Returns:
            float: Total volume in cubic centimeters

        Note:
            - Considers product fit ratios
            - Used in box selection
            - Helps optimize packing
        """
        return sum([item.volume() for item in self.items])

    def get_total_weight(self):
        """
        Calculates total weight of all pending products.
        Used for weight limit compliance.

        Returns:
            float: Total weight in grams

        Note:
            - Critical for box selection
            - Ensures weight limits
            - Considers all pending items
        """
        return sum([item.weight for item in self.items])
    
    def get_dimensions(self):
        """
        Analyzes maximum dimensions across all products.
        Used for box compatibility checking.

        Returns:
            List[float]: [max_width, max_height, max_length] in cm

        Note:
            - Considers all orientations
            - Used in box selection
            - Ensures product fit
        """
        sorted_dimensions = sorted(
            [(item.width, item.height, item.length) for item in self.items],
            key=lambda dims: sorted(dims, reverse=True),
            reverse=True
        )
        return [
            max([dims[0] for dims in sorted_dimensions]),
            max([dims[1] for dims in sorted_dimensions]),
            max([dims[2] for dims in sorted_dimensions])
        ]
    
    def take_item(self):
        """
        Removes and returns the next product for packing.
        Manages product state transition.

        Returns:
            Product: Next product to pack, or None if empty

        Note:
            - Updates product status
            - Maintains packing order
            - Tracks taken items
        """
        if len(self.items) > 0:
            item = self.items.pop(0)
            self.taken_items.append(item)

            return item
        
        return None

    def take_specific_item(self, item):
        """
        Removes an item from the order -> str:.

        Args:
            item (Product): The item to be removed from the order.
        """
        if (item in self.items):
            self.items.remove(item)
            self.taken_items.append(item)
            return item
        
        return None

    def secure_packed_items(self):
        """
        Finalizes successfully packed items.
        Manages product state transition.

        Note:
            - Moves items to packed list
            - Clears taken items list
            - Tracks packing success
            - Final state for products
        """
        self.packed_items.extend(self.taken_items)
        self.taken_items = []

    def get_order_number(self):
        """
        Retrieves the order's unique identifier.

        Returns:
            str: Order number

        Note:
            - Used for tracking
            - Links to external systems
            - Identifies packing results
        """
        return self.order_number