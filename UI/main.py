import sys
sys.dont_write_bytecode = True

import import_classes
modules = import_classes.import_all_modules_in_current_folder()

# Dynamically get the classes from the respective modules
Order = getattr(modules['order'], 'Order', None)
Box = getattr(modules['box'], 'Box', None)
Item = getattr(modules['item'], 'Item', None)

if Order and Box and Item:
    # Create an order
    order = Order(order_id=101)

    # Create boxes
    box1 = Box(box_id=1)
    box2 = Box(box_id=2)

    # Create items
    item1 = Item(name="Laptop", weight=2.5)
    item2 = Item(name="Phone", weight=0.5)
    item3 = Item(name="Book", weight=1.0)

    # Add items to boxes
    box1.add_item(item1)
    box1.add_item(item2)

    box2.add_item(item3)

    # Add boxes to the order
    order.add_box(box1)
    order.add_box(box2)

    # Print the order to see the hierarchy
    print(order)
else:
    print("Failed to retrieve Order, Box, or Item classes.")
