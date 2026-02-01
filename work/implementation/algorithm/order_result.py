class OrderResult:
    """
    Stores and manages the results of packing an order into boxes.
    This class acts as a container for the packing results and provides
    methods to access and format the packing solution.

    The result system tracks:
    - The original order being packed
    - All boxes used for the order
    - Product positions within each box
    - Packing coordinates and orientations

    Attributes:
        order (Order): The original order being packed
        boxes (List[BoxResult]): List of boxes used to pack the order's products
        
    Key Features:
        - Maintains order-box relationships
        - Tracks all product placements
        - Provides CSV output formatting
        - Supports visualization data export
        - Maintains packing solution integrity

    Example Usage:
        order_result = OrderResult(order)
        order_result.add_box(packed_box)
        csv_output = order_result.get_csv_result()
    """

    def __init__(self, order):
        """
        Initializes a new order result container.
        
        Args:
            order (Order): The order being packed

        Note:
            - Stores reference to original order
            - Initializes empty box list
            - Prepares for result tracking
        """
        self.order = order
        self.boxes = []

    def add_box(self, box):
        """
        Adds a packed box to the order result.
        Used to build up the complete packing solution.
        
        Args:
            box (BoxResult): A box containing packed products

        Note:
            - Maintains box order for reporting
            - Each box contains product positions
            - Used during packing process
        """
        self.boxes.append(box)

    def get_boxes(self):
        """
        Retrieves all boxes used in the packing solution.
        
        Returns:
            List[BoxResult]: List of all boxes used for this order

        Note:
            - Returns boxes in packing order
            - Each box contains placement details
            - Used for solution analysis
        """
        return self.boxes

    def get_order(self):
        """
        Retrieves the original order being packed.
        
        Returns:
            Order: The order associated with these results

        Note:
            - Provides access to order details
            - Used for result validation
            - Maintains order reference
        """
        return self.order

    def get_csv_result(self):
        """
        Generates a CSV-formatted string of the packing results.
        Includes detailed placement information for each product.

        Returns:
            str: CSV formatted packing results with format:
                OrderID,BoxID,BoxType,BoxDimensions,ProductInfo,Coordinates

        Note:
            - Includes all product placements
            - Contains box information
            - Shows exact coordinates
            - Includes rotation data
            - Used for output and visualization
        """
        csvResult = []
        orderId = self.order.get_order_number()

        for boxResult in self.boxes:
            boxResultId = boxResult.get_box_id()
            boxDefinition = boxResult.get_box_definition()

            for itemPosition in boxResult.get_all_coordinates():
                coordinates = itemPosition.get_coordinates()
                product = itemPosition.get_product()
                rotation = itemPosition.get_rotation()

                dimensions = product.get_dimensions()
                adjustedDimensions = rotation.adjust_dimensions(*dimensions)

                csvResult.append(f"{orderId},{boxResultId},"
                               f"{boxDefinition.get_box_type()},"
                               f"{','.join(map(str, boxDefinition.get_box_dimensions()))},"
                               f"{product.get_product_name()},"
                               f"{','.join(map(str, adjustedDimensions))},"
                               f"{','.join(map(str, coordinates))}")

        return "\n".join(csvResult)


    