import csv
from .box import Box
from .item import Item
from .order import Order

class Reader:
    """
    Handles the reading and loading of orders, boxes, and items from a CSV file.
    """

    def load_orders_from_csv(self, csv_file_path, min_boxes = 0):
        """
        Reads orders, boxes, and items from a CSV file and constructs the corresponding objects.

        Parameters:
        - csv_file_path (str): The file path to the CSV file containing the order data.

        Returns:
        - list: A list of `Order` objects, each containing associated `Box` and `Item` objects.

        CSV File Structure:
        The CSV file must include the following columns:
        - Order ID: Unique identifier for each order.
        - Box ID: Unique identifier for each box within an order.
        - Box Width, Box Height, Box Depth: Dimensions of the box.
        - Box Type: A string identifying the type or description of the box.
        - Item Name: Name of the item being placed in the box.
        - Item Width, Item Height, Item Depth: Dimensions of the item.
        - Item Position X, Item Position Y, Item Position Z: Position of the item inside the box.
        """
        orders = {}  # Dictionary to store orders by their IDs

        with open(csv_file_path, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Extract data for each row
                order_id = str(row['Order ID'])  # Order ID
                box_id = str(row['Box ID'])  # Box ID
                box_type = row['Box Type']  # Box Type


                # Box dimensions: Depth (Length), Width, Height
                box_dimensions = [
                    float(row['Box Depth']),  # Length
                    float(row['Box Width']),  # Width
                    float(row['Box Height'])  # Height
                ]

                # Ensure the order exists in the orders dictionary
                if order_id not in orders:
                    orders[order_id] = Order(order_id)

                order = orders[order_id]

                # Ensure the box is added to the order
                if not any(box.box_id == box_id for box in order.get_boxes()):
                    box = Box(box_id, box_dimensions, box_type)
                    order.add_box(box)

                # Extract item data
                item_name = row['Item Name']  # Item Name

                item_dimensions = [
                    float(row['Item Depth']),  # Length
                    float(row['Item Width']),  # Width
                    float(row['Item Height'])  # Height
                ]
                item_position = [
                    float(row['Item Position Z']),  # X (Width)
                    float(row['Item Position X']),  # Y (Height)
                    float(row['Item Position Y'])  # Z (Depth/Length)
                ]

                # Create the Item object
                item = Item(
                    name=item_name,
                    weight=0,  # Assuming weight isn't in the CSV
                    dimension=item_dimensions,
                    position=item_position
                )

                # Add the item to the box
                box.add_item(item)

        filtered_orders = {order_id: order for order_id, order in orders.items() if len(order.get_boxes()) > min_boxes}

        return list(filtered_orders.values())

