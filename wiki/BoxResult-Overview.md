## Purpose
The `BoxResult` class manages the results of packing products into a specific box. It serves as a bridge between the packing algorithm and the physical representation of a packed box, ensuring all products are placed efficiently while tracking those that cannot be placed.

## Key Responsibilities
* Manages layers of products within the box.
* Tracks oversized products that cannot fit in the box.
* Monitors leftover products that couldn’t be packed due to space constraints.
* Provides utilities for collision detection and efficient placement.

## Attributes
1. `box`
Type: BoxDefinition
Purpose: Defines the box's physical dimensions and properties, serving as a container for products.
2. `layers`
Type: List[LayerResult]
Purpose: Tracks all layers within the box. Each layer contains products packed in a single horizontal plane.
3. `oversized_product]`
Type: List[Product]
Purpose: Stores products that are too large to fit in the box under any orientation.
4. `leftover_products`
Type: List[Product]
Purpose: Stores products that could not be placed in the box due to space constraints.


## Key Methods

### 1. `pack_products_by_order(order: Order)`

**Purpose**: Packs products from an `Order` into the box using a layer-based approach.

**Process**:
1. Orders items for optimal packing (e.g., by size or priority).
2. Iteratively attempts to place each product in existing layers.
3. Creates new layers as needed.
4. Tracks rejected products (oversized or leftover).

**Reasoning**:
- **Why this way?** Layer-based packing simplifies a complex 3D packing problem into smaller, manageable 2D problems. Each layer acts as an independent packing plane.
- **Alternatives**: A full 3D bin packing algorithm would provide theoretically better utilization but would:
  1. Require significantly more computational resources.
  2. Increase complexity in handling overlapping products and stability issues.

**Code Snippet**:
```python
def pack_products_by_order(self, order: Order):
    """
    Packs products from an order into this box using a layer-based approach.
    
    Args:
        order (Order): The order containing products to pack
    """
    self.order = order
    self.order.order_items()

    while True:
        product = self.order.take_item()

        if not product:  # All items have been processed
            break

        if not self.add_product_to_box(product):
            logging.warning(f"Product {product.get_product_name()} could not be packed into the box.")
            self.order.add_rejected_item(product)
```


### 2. `product_is_oversized(product: Product)`

**Purpose**: Checks if a product exceeds the box dimensions in all possible orientations.

**Reasoning**:
- **Why this way?** Early detection of oversized products avoids wasting time trying to place them in layers. The method considers all possible rotations, ensuring no viable configuration exists.
- **Alternatives**:
  - Direct rejection of products based on unrotated dimensions. However, this would fail for products that only fit under specific orientations.
  - Allowing oversized products into packing attempts would add unnecessary complexity and increase the likelihood of invalid placements.

**Code Snippet**:
```python
def product_is_oversized(self, product):
    """
    Determines if a product is too large for this box.
    
    Args:
        product (Product): Product to check
    
    Returns:
        bool: True if product is too large for the box, False otherwise
    """
    return any(
        dim > max_dim 
        for dim, max_dim in zip(sorted(product.get_dimensions()), sorted(self.box.get_box_dimensions()))
    )
```

### 3. `add_product_to_box(product: Product)`

**Purpose**: Attempts to add a product to the box.

**Process**:
1. Checks if the product is oversized.
2. Tries to place the product in existing layers.
3. Creates a new layer if no existing layer fits.

**Reasoning**:
- **Why this way?**
  - Using existing layers prioritizes efficient utilization of available space.
  - Dynamically creating layers ensures flexibility in handling diverse product dimensions.
- **Alternatives**:
  - Restrict packing to predefined layers, leading to wasted vertical space.
  - A purely volumetric packing algorithm could theoretically achieve better results but would lose the stability benefits of layer-based packing.

**Code Snippet**:
```python
def add_product_to_box(self, product):
    """
    Attempts to add a product to the box using the layer-based packing strategy.
    
    Args:
        product (Product): Product to place in the box
    
    Returns:
        bool: True if product was successfully placed, False otherwise
    """
        if self.product_is_oversized(product):
            self.oversized_products.append(product)
            logging.warning(f"Product {product.item} is too large to fit in the box.")
            return False

        existing_coordinates = self.collect_existing_coordinates()

        # Wrap product in a Position object
        rotation = RotationType.initial_rotation(product.width, product.height, product.length)
        position = Position(product, 0, 0, 0, rotation)

        logging.debug(f"Position for product {product.item}: {position}, Coordinates: {position.get_coordinates()}")

        # Try to place the product in existing layers
        for idx, layer in enumerate(self.layers):
            logging.debug(f"Attempting to place product {position.get_product().item} in Layer {idx + 1}.")
            if layer.add_product(position, existing_coordinates):
                logging.debug(f"Product {product.item} successfully placed in Layer {idx + 1}.")
                return True

        # If no existing layer fits, create a new layer
        if self.add_new_layer(position, existing_coordinates):
            logging.debug(f"Product {product.item} successfully added to a new layer.")
            return True

        # Mark the product as leftover if no fit
        self.leftover_products.append(product)
        logging.warning(f"Product {product.item} could not be placed in any layer.")
        return False
```


### 4. `def collect_existing_coordinates(self):`

**Purpose**: Collects the coordinates of all placed products for collision detection.

**Reasoning**:
- **Why this way?** Dynamically collecting product coordinates ensures real-time validation of potential overlaps.
- **Alternatives**:
  - Precomputing potential coordinates for all placements would require significant memory overhead and limit flexibility.


## Code Snippet
```python
def collect_existing_coordinates(self):
    """
    Collects coordinates of all products currently placed in the box.
    
    Returns:
        List[tuple]: List of (product_id, x, y, z, width, height, length)
                     for each placed product
    """
    existing_coordinates = []
    for layer in self.layers:
        existing_coordinates.extend(layer.get_product_coordinates())
    return existing_coordinates
```

# Core logic

### 1. Layer Creation

**Purpose**: Automatically creates a new layer if no existing layer can accommodate a product.

**Reasoning**:
- **Why this way?** Dynamically creating layers ensures the algorithm adapts to varying product sizes and maximizes the box's vertical space utilization.
- **Alternatives**:
  - Predefining layers would lead to inefficient space usage for irregularly shaped products.

**Code Snippet**:
```python
def add_new_layer(self, position, existing_coordinates):
    """
    Creates and initializes a new packing layer in the box.
    
    Args:
        position (Position): Initial product position for the layer
        existing_coordinates (List[tuple]): Coordinates of already placed products
    
    Returns:
        bool: True if layer was created and product placed, False otherwise
    """
    new_layer_base_height = sum(layer.layer_height for layer in self.layers)
    remaining_height = self.box.height - new_layer_base_height

    if remaining_height >= min(position.product.get_dimensions()):
        new_layer = LayerResult(self.box, base_height=new_layer_base_height)

        if new_layer.add_product(position, existing_coordinates):
            self.layers.append(new_layer)
            return True

    return False
```

## 2. Collision Detection
**Purpose**: Ensures that products do not overlap within the box.

**Reasoning**:
- **Why this way?** Comparing dimensions and coordinates ensures no invalid placements occur during packing.
- **Alternatives**:
  - Avoiding collision checks entirely would result in overlapping products and an invalid packing solution.

```python
def check_collision(new_position, existing_coordinates):
    """
    Detects if a new product placement overlaps with existing products.
    
    Args:
        new_position (Position): The proposed placement position
        existing_coordinates (List[tuple]): Existing product positions
    
    Returns:
        bool: True if there is a collision, False otherwise
    """
    new_x, new_y, new_z = new_position.get_coordinates()
    new_width, new_height, new_length = new_position.get_dimensions()

    for coord in existing_coordinates:
        product_id, x, y, z, width, height, length = coord
        if (
            new_x < x + width and new_x + new_width > x and
            new_y < y + height and new_y + new_height > y and
            new_z < z + length and new_z + new_length > z
        ):
            return True

    return False
```
