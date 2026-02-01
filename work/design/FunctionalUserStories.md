
# User Stories and System Requirements

## System

**As a System, I want to be able to:**
- Start the process in order to pack all orders.
- Reset the process in order to fix issues.

## Product Input Reader

**As a Product Input Reader, I want to be able to:**
- Read a CSV file in order to load data into the System.
- Output data in order to be used by other components.

## Order Input Reader

**As a Order Input Reader, I want to be able to:**
- Read a CSV file in order to load order data into the System.
- Output processed data in order to enable further use.

## Box Input Reader

**As a Box Input Reader, I want to be able to:**
- Read a CSV file in order to load box data into the System.

## BoxDefinition

**As a Box Definition, I want to be able to:**
- Calculate if a product fits in the box in order to find a suitable size.
- Determine the min and max volume in order to pick the right box size.

## Layer Node

**As a Layer Node, I want to be able to:**
- Use pivot points in order to verify if a product fits in the layer.
- Maintain a list of products in order to inform other components.
- Calculate the unused volume of the layer in order to manage space.

## Packer

**As a Packer, I want to be able to:**
- Select the best box for each order in order to match weight, volume, and dimensions.
- Add products in order to fill all items in the box.
- Reposition products in order to fit them in the current layer.
- Initialize new layers in the box as needed in order to fit products.
- Place products by size in order to optimize the packing process.
- Place products according to an algorithm in order to enhance packing efficiency.
- Select a product in order to place all items in the box.
- Check if a product fits in order to find the best option.

## Best Fit Decreasing

**As a Best Fit Decreasing algorithm, I want to be able to:**
- Check if a product fits within a box in order to make the correct selection.
- Place products in the box in order to complete the order.

## Order Manager

**As an Order Manager, I want to be able to:**
- Sort orders by volume according to the algorithm in order to create a clear packing structure.
- Load products in order to make the product data available for processing.
- Load orders in order to make order data available for processing.
- Group orders by unique identifiers in order to organize and manage packing.

## Order 

**As an Order, I want to be able to:**

-Add an item to an order in order to include it in the packing process.
- Add multiple items to an order in order to include them for packing.
- Add a rejected item to an order in order to manage items that cannot be packed.
- Reset rejected items in order to clear and start fresh.
- Reset all items in order to clear the entire order.
- Order items according to the algorithm in order to optimize the packing process.
- Retrieve the list of items in an order in order to view them.
- Take an item from an order in order to process it for packing.
- Take a specific item from an order in order to handle a specific product.
- Retrieve the order number in order to track and manage the order.