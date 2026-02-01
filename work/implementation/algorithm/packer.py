import logging
from .box_result import BoxResult
from .order_result import OrderResult

class Packer:
    """
    The Packer class implements the core 3D bin packing algorithm, responsible for efficiently 
    packing products into appropriate boxes while respecting all constraints.

    The packing algorithm follows these key principles:
    1. Box Selection: Choose the smallest suitable box that can fit the order
    2. Layer-based Packing: Pack products in horizontal layers for stability
    3. Space Optimization: Minimize wasted space and ensure efficient volume utilization
    4. Weight Distribution: Consider weight limits and distribution

    Attributes:
        order (Order): Current order being packed
        orderResults (List[OrderResult]): Results of all packed orders
        available_boxes (List[BoxDefinition]): Available box types for packing
        coordinates_products (List[Dict]): Tracking of product positions
        box_position (BoxResult): Current box being packed

    Key Algorithms:
        - Initial Box Selection: Chooses optimal starting box size
        - Layer-based Packing: Organizes products in horizontal layers
        - Box Upgrading: Switches to larger box when needed
        - Volume Optimization: Maximizes space utilization
    """

    def __init__(self):
        """
        Initializes a new Packer instance with empty state.
        """
        self.order = None
        self.orderResults = []
        self.available_boxes = []
        self.coordinates_products = []
        self.box_position = None

    def initial_box_selection(self, lastBox=None):
        """
        Selects the optimal initial box for packing the current order.
        
        The selection algorithm considers:
        1. Total order volume and weight
        2. Maximum product dimensions
        3. Box fill percentage constraints
        4. Previous box selection (for optimization)

        Args:
            lastBox (BoxDefinition, optional): Previously used box, for optimization

        Returns:
            BoxDefinition: Selected box for packing

        Notes:
            - Skips undersized boxes and multi-order boxes
            - Considers minimum fill requirements
            - Falls back to smallest box if no suitable box found
        """
        total_volume = self.order.get_total_volume()
        total_weight = self.order.get_total_weight()

        if lastBox == self.sorted_boxes[-1]:
            return lastBox

        ignore = 2
        toReturn = None
        dimensions = self.order.get_dimensions()

        for box in self.sorted_boxes:
            ignore = ignore - 1

            if "Undersized" in box.description or "Multi" in box.description:
                continue

            toReturn = box

            if lastBox != None:
                if box.max_volume() <= lastBox.max_volume():
                    continue

            if (box.max_volume() > 1):
                if box.fits_within(total_volume, total_weight):
                    if box.fits_with_dimensions(dimensions):
                        return box
                else:
                    if ignore == 0 and total_volume < box.min_volume():
                        return self.sorted_boxes[0]
                
        self.box_position = BoxResult(toReturn)

        return toReturn


    def pack_order(self, order, available_boxes=[]):
        """
        Main packing algorithm that processes an order and packs it into appropriate boxes.
        
        The algorithm follows these steps:
        1. Initialize order and available boxes
        2. Sort boxes by volume for efficient selection
        3. Attempt to pack order into smallest suitable box
        4. If packing fails, try next larger box
        5. Continue until all products are packed or largest box is reached

        Args:
            order (Order): The order to be packed
            available_boxes (List[BoxDefinition]): Available box types

        Returns:
            str: CSV formatted packing results

        Raises:
            Exception: If products cannot fit in any available box

        Notes:
            - Handles oversized products
            - Manages box transitions
            - Tracks packing success/failure
        """
        self.orderResults.append(OrderResult(order))
        self.order = order
        self.available_boxes = available_boxes
        self.sorted_boxes = sorted(self.available_boxes, 
                                 key=lambda box: box.max_volume(), 
                                 reverse=False)

        isSuccesfull = False
        shouldUseNextBox = True
        lastBox = None
        packed_items = 0

# region calling of the algorithm
        while isSuccesfull == False:
            shouldUseNextBox = True
            
            fittingBox = self.initial_box_selection(lastBox)

            if fittingBox == self.sorted_boxes[-1]:
                shouldUseNextBox = False

            lastBox = fittingBox

            boxResult = BoxResult(fittingBox)
            boxResult.pack_products_by_order(self.order)
            # boxResult.pack_products(self.order.get_items())

            if not shouldUseNextBox and len(boxResult.get_oversized_products()) > 0:
                # Should only happen if an item exceeds the largest box's dimensions
                raise Exception("Some products do not fit in any of the available boxes.")

            leftover_items = boxResult.get_leftover_products()
            isSuccesfull = len(leftover_items) == 0
            if isSuccesfull or not shouldUseNextBox:
                self.order.secure_packed_items()
                self.order.reset_rejected_items()
                self.orderResults[-1].add_box(boxResult)
                order_items = len(order.packed_items)
                logging.debug(f"{boxResult.box.description} {order_items - packed_items}")
                packed_items = order_items
                shouldUseNextBox = True
                lastBox = None
            else:
                self.order.reset_all_items()
# endregion

        return self.get_packer_csv_result()
    
    def get_packer_csv_result(self):
        """
        Generates a CSV-formatted string containing the packing results.
        
        The output includes:
        - Order information
        - Box selections
        - Product positions and orientations
        - Packing coordinates

        Returns:
            str: CSV formatted packing results with detailed placement information

        Note:
            Format: OrderID,BoxID,BoxType,ProductInfo,Coordinates,...
        """
        returnValue = []

        for orderResult in self.orderResults:
            returnValue.append(orderResult.get_csv_result())
        
        return "\n".join(returnValue)
