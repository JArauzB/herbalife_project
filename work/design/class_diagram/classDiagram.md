# Class Diagram Explanation

## Color Legend
- **Light Blue**: Input readers (data loading)
- **Light Green**: Core processing classes
- **Light Yellow**: Data entities (products, orders, boxes)
- **Light Purple**: Algorithms
- **Light Orange**: Helper classes

---

## Class Descriptions

# Class Explanations

### 1. Order

- **Attributes**:
  - **items**: A list that contains all the products in a particular order, representing everything included in a single transaction or shipment.
  - **orderNumber**: A unique identifier assigned to each order, helping to distinguish this order from others in the system.
  - **dateTime**: (Optional) Stores the date and time when the order was created, providing a timestamp that may be useful for tracking or sorting.

- **Methods**:
  - **itemCount()**: Counts and returns the number of items in the `items` list for this order. For example, if there are 5 products in the order, this method will return 5. This helps in quickly identifying the size or scale of each order.

- **Relationships**:
  - **Aggregates Products**: `Order` aggregates multiple `Product` instances, meaning that it "owns" a collection of products associated with that order. This relationship is known as an **aggregation relationship**, where `Order` serves as a container for related `Product` items but does not define them exclusively.
  - **Interacts with OrderManager**: The `OrderManager` class uses `Order` to manage and organize the collection of orders, aiding in tasks such as sorting or processing these orders as part of the packing workflow.

---

### 2. OrderResult

- **Attributes**:
  - **orderNumber**: A unique identifier that matches the order’s ID from `Order`, used to keep track of which result corresponds to which order.
  - **boxes**: An array (or list) containing all the `Box` instances used to pack the items in this order. If an order requires multiple boxes, each box is added to this list.
  - **itemPosition**: Tracks the position of each item within the packing process, showing where each product is placed inside the boxes. This attribute ensures that every product's location is known, which can be useful for unpacking or retrieval.

- **Relationships**:
  - **Aggregates Boxes**: `OrderResult` collects multiple `Box` instances, meaning that each `OrderResult` can represent an order packed into one or more boxes. This **aggregation relationship** helps manage large orders that require multiple boxes to be fully packed.

---

### 3. LayerResult

- **Attributes**:
  - **pivotPoint**: A set of 3D coordinates (represented as a tuple) that defines the starting position of the layer within the box. This is the origin point for the layer’s layout and helps position it relative to other layers.
  - **products**: A list of `Product` items that are placed on this specific layer. This attribute groups all products that fit within the same horizontal level inside the box.
  - **layerHeight**: The height of this layer, based on the tallest product within it. The `layerHeight` helps determine the amount of vertical space this layer takes up, which is crucial for stacking layers efficiently within the box.

- **Methods**:
  - **doesFit(product: Product) -> bool**: Checks if a given product can fit within the current layer based on the remaining available space. This method ensures that products are added only if they meet the layer’s size constraints.
  - **layerVolume() -> float**: Calculates the total volume occupied by all products in the layer. This value helps evaluate how much space each layer uses within the box, aiding in maximizing packing efficiency.

- **Relationships**:
  - **Contained in Box**: `LayerResult` instances are aggregated within the `Box` class, where each `Box` is made up of several `LayerResult` layers stacked on top of each other. This **composition relationship** signifies that `LayerResult` instances exist only as parts of a `Box`, and they are integral to the box’s internal structure.
  - **Organizes Products within Box**: Each `LayerResult` is responsible for arranging `Product` instances at a particular layer within the box. By managing products on a layer-by-layer basis, `LayerResult` helps the `Box` maintain a well-structured and efficient packing layout.

---

### 3. LayerResult
- **Attributes**:
  - **pivotPoint**: This is a set of 3D coordinates (`x`, `y`, `z`) that represents where this layer starts inside the box. 
  - **products**: A list of `Product` items that are placed on this layer. So, all the products that fit on the same horizontal level inside the box are grouped here.
  - **layerHeight**: The height of this layer, which is usually determined by the tallest product on the layer. This helps us keep track of how much vertical space the layer occupies inside the box.
- **Methods**:
  - `doesFit(product: Product) -> bool`: This method checks if a given product can fit into this layer without exceeding the layer's remaining space. 
  - `layerVolume() -> float`: Calculates the total volume occupied by this layer. 
- **Relationship**:
  - **Relationship with Box**: Each `Box` is composed of multiple `LayerResult` instances. You can think of a `Box` as being made up of several layers stacked on top of each other, and each layer is represented by a `LayerResult`. So, the `Box` class has a collection of `LayerResult` objects that define its internal structure.
    - This relationship is a **composition**, meaning that the `LayerResult` cannot exist independently without the `Box`. If the `Box` is destroyed or discarded, its layers (the `LayerResult` instances) are also destroyed. They are tightly bound to the lifecycle of the `Box`.
  - **Interaction with Products**: The `LayerResult` organizes how products are placed within a layer inside the box. It manages the placement and arrangement of products on that specific layer, ensuring they fit together efficiently without exceeding the layer's boundaries.
    - Products are added to layers based on whether they fit (`doesFit` method) and the available space. The `LayerResult` keeps track of the products it contains and their positions relative to the `pivotPoint`.
  - **Overall Role in Packing**: By dividing the box into layers (`LayerResult`s), the packing process becomes more organized. The `Packer` class can focus on filling one layer at a time, stacking layers as needed.

---

### 4. Box

- **Attributes**:
  - **layers**: A list of `LayerResult` instances representing the different layers inside the box. Each `LayerResult` is like a level within the box, containing products organized at that specific height. 

- **Methods**:
  - **addLayer(layer: LayerResult) -> void**: This method adds a new layer (`LayerResult`) to the box. When packing, we may need to add a new layer if the current layer is full or if the next product doesn’t fit in the existing space. Adding a layer means we’re increasing the vertical organization of products inside the box, like adding another row in a stack.
  - **getItemPosition()**: Retrieves the position of items within the box. This method is used to locate where each product is placed within the box’s internal structure. It’s helpful for determining and visualizing how items are arranged and understanding the spatial layout of products within each layer.

- **Relationships**:
  - **Composition with LayerResult**: 
    - The `Box` class is composed of multiple `LayerResult` instances, where each `LayerResult` represents a distinct layer of products. In this relationship, the `Box` "owns" its `LayerResult`s in a way that implies the layers cannot exist independently outside of the box. This means that if the `Box` is deleted or removed, all the `LayerResult` instances within it are also destroyed.
    - Each `Box` is effectively a collection of layers, stacked from bottom to top. This composition relationship allows the `Box` to maintain a clear, organized structure, where products are divided across layers and each layer has its own internal organization of items. It’s as if each `Box` is made up of several "shelves," with each `LayerResult` acting as a shelf holding a certain set of products.

  - **Interaction with LayerResult**:
    - `LayerResult` instances are organized within the `Box` to maintain an efficient packing layout. When items are placed inside the box, they are grouped within these layers to ensure optimal use of space. The `Box` relies on `LayerResult`s to help arrange products systematically, layer by layer, allowing the packing algorithm to focus on filling one level before moving up to the next.
    - The `addLayer` method plays a key role in managing the layers within the `Box`. As products are added and space runs out on the current layer, a new `LayerResult` is created and added, ensuring that the packing process flows smoothly from one layer to the next.

  - **Overall Role in Packing**:
    - The `Box` class acts as the container that holds and organizes all products for a particular order. By dividing the space within the box into layers (`LayerResult`s), the packing process becomes more systematic. The `Packer` class can focus on filling the box one layer at a time, making it easy to keep track of available space and ensuring that items fit without overlapping.
    - Imagine packing a suitcase where each `LayerResult` is a layer of folded clothes. As you pack, you add layers, keeping each row of items organized and compact. The `Box` class manages these layers, helping you make the most of the available space within the container.

---

### 5. Position

- **Attributes**:
  - **product**: The `Product` instance that is placed at this specific position within the box. This attribute links a product to its precise location, helping us track which product occupies this particular spot in the box.
  - **location_x, location_y, location_z**: These are floating-point values representing the 3D coordinates of the product within the box. They provide the exact position in terms of `x`, `y`, and `z` axes. 
  - **rotation**: A `RotationType` attribute that specifies the orientation of the product at this position. In packing, items can often be rotated to fit better, and this attribute captures whether the product has been rotated and in which direction. It’s essential for ensuring that products are oriented correctly to optimize space usage.

- **Purpose**:
  - **Spatial Information**: The `Position` class provides detailed spatial information about where each product is placed inside the box, allowing for precise organization of items. With its 3D coordinates and rotation details, it helps ensure that products fit within the box without overlapping or leaving unused spaces.
  - **Tracking Product Layout**: By using `Position`, we can accurately track each product’s placement within the box, making it easier to visualize the layout. This information is useful not just for the packing process, but also for unpacking or finding specific products in an organized manner once packed.

- **Relationships**:
  - **Association with Product**: Each `Position` instance is directly associated with a single `Product`. This means that each `Position` entry refers to a specific product within the box, holding details about its exact placement and orientation. The relationship is essential for connecting each product to its spatial data.
  - **Role within the Box Structure**:
    - The `Position` class plays a supporting role within the box structure by providing low-level details about the placement of products. While the `Box` and `LayerResult` classes organize products in layers, `Position` handles the finer details of exactly where each product sits within its layer.
    - Each `LayerResult` or `Box` contains multiple `Position` instances, each representing a product's spot within that layer or box. This makes `Position` a crucial component for achieving a detailed, organized layout within the packing system.
  
---

### 6. Product

- **Attributes**:
  - **width, height, length**: These are the physical dimensions of the product, represented as floating-point numbers. They define the product’s size along each axis (width for `x`, height for `y`, and length for `z`). This information is essential for determining whether the product will fit within a given space in the box and for calculating its volume.
  - **weight**: The product’s weight, also a floating-point number. Weight is important for packing because there may be weight limits per box, and certain products might need to be packed more securely if they are heavy.
  - **item**: An identifying string for the product. 

- **Methods**:
  - **volume() -> float**: This method calculates the volume of the product by multiplying its width, height, and length. The volume is crucial for packing, as it determines how much space the product will occupy within a box. The `volume` calculation helps in deciding the most efficient way to fit the product inside the box along with other items.

- **Relationships**:
  - **Created by ProductInputReader**: The `Product` class instances are generated by the `ProductInputReader`, which reads product data from an external source (like a file) and converts it into `Product` objects. This relationship means that `ProductInputReader` serves as the initial source of product information in the system, preparing products to be packed.
  - **Used by Packer and LayerResult**:
    - **Packer**: The `Packer` class uses `Product` instances as the core items to be packed into boxes. The `Packer` relies on the dimensions and weight of each `Product` to determine the best way to organize items within each box.
    - **LayerResult**: Within each `LayerResult` (or layer) inside a box, products are arranged and organized. The `LayerResult` class utilizes the dimensions of `Product` instances to place them in layers, ensuring they fit together effectively within the limited space of each layer.

- **Overall Role in Packing**:
  - The `Product` class is fundamental to the packing system because it represents the individual items being packed. Each `Product` has specific characteristics (dimensions and weight) that influence how it’s organized in a box. Understanding these characteristics helps the system maximize the space within boxes and meet any weight restrictions.

---

### 7. ProductInputReader

- **Attributes**:
  - **file_path**: A string that represents the path to the file containing product data.  

- **Methods**:
  - **interpret_data(data: str) -> list[Product]**: This method takes raw data in the form of a string (like a line from a file) and converts it into a list of `Product` objects. This is helpful for processing data from sources that aren’t strictly formatted, such as plain text input or direct string data.
  - **read_csv(file: str) -> list[Product]**: Reads data from a CSV file located at `file_path`. It parses each line of the file, interprets it, and then converts it into `Product` instances, which are then ready to be used by other parts of the system. This method specifically handles CSV-format data, making it easier to process structured information in bulk.
  - **group_by_order(products: list[Product]) -> dict[str, list[Product]]**: This method takes a list of `Product` objects and organizes them by order, grouping products that belong to the same order number. It returns a dictionary where the key is the order number (as a string) and the value is a list of `Product` instances belonging to that order. This is useful for cases where we need to process products in order-based batches.

- **Relationships**:
  - **Creates Product Instances**: `ProductInputReader` is responsible for creating `Product` objects. It reads raw data from files or strings, interprets that data, and then generates instances of `Product` based on the information it finds. This relationship is crucial because it means `ProductInputReader` serves as the initial source of `Product` instances in the system, ensuring that product data is correctly loaded and organized before being used elsewhere.
  - **Loads Products into the System**: The `ProductInputReader` not only creates `Product` instances but also prepares them for the packing process by organizing them into a structured format. This makes it easier for other classes (like `OrderManager` or `Packer`) to access and work with the products. Essentially, it acts as a bridge between raw data and usable `Product` objects within the system, making sure that product information flows smoothly into the packing process.

- **Overall Role in Packing**:
  - The `ProductInputReader` class is the "data loader" for products. It takes raw data files, interprets them, and produces clean, usable `Product` objects. 

---

### 8. BoxInputReader

- **Methods**:
  - **load_boxes(file: str) -> list[BoxDefinition]**: Reads box definitions from a specified file and returns a list of `BoxDefinition` instances. This provides the packing system with all the available box types and their specifications.

- **Relationships**:
  - **Creates BoxDefinition Instances**: `BoxInputReader` is responsible for loading and creating `BoxDefinition` objects from external data, which are then used by the packing process to understand box constraints and characteristics.

---

### 9. System

- **Attributes**:
  - **output_data**: An array that stores the final output data produced by the system, often containing the results of the packing process.
  - **product_data**: A list of `Product` instances that have been loaded into the system, representing all products that need to be packed.
  - **box_definitions**: A list of `BoxDefinition` objects that define the different types of boxes available for packing, including their constraints and dimensions.

- **Methods**:
  - **init()**, **reset()**: Initialize or reset the system data, preparing it for a new packing operation. These methods ensure that previous data does not interfere with new processes.
  - **read_box_csv(file: str)**: Reads box data from a CSV file and populates the `box_definitions` attribute with `BoxDefinition` instances, making various box types available for the packing process.
  - **read_product_csv(file: str)**: Reads product data from a CSV file, processes it, and loads it into the `product_data` list, providing the system with all products to be packed.
  - **send_to_packer(box: Box)**: Sends a specific `Box` instance to the `Packer` class for item placement, enabling the packing process to begin on that box.
  - **start_process()**: Initiates the packing process once all data has been loaded and validated, setting off a sequence of operations managed by the system.
  - **validateData() -> bool**: Checks if the loaded product and box data meet required formats and constraints for successful packing. Returns `true` if data is valid, `false` otherwise.

- **Relationships**:
  - **Uses ProductInputReader, BoxInputReader, and Packer**: The `System` class orchestrates the entire packing process by using `ProductInputReader` to load product data, `BoxInputReader` to load box definitions, and `Packer` to handle the actual packing operations. This combination ensures that all data is prepared, validated, and efficiently packed.

- **Overall Role in Packing**:
  - The `System` class serves as the central controller for the packing process. It coordinates the loading of products and boxes, initiates the packing sequence, and validates data before passing it to other components. This class ensures that all parts of the system work together smoothly, from data input to final packed output.

---

### 10. BoxDefinition

- **Attributes**:
  - **height, width, length, weight**: Physical dimensions and weight of the box.
  - **max_weight**: Maximum allowable weight the box can safely hold.
  - **description, container_type, remark**: Metadata providing details about the box type, usage recommendations, and additional remarks.
  - **max_fill_percentage, min_fill_percentage**: Constraints on how full the box should be, representing maximum and minimum fill limits for efficient and safe packing.

- **Methods**:
  - **min_volume() -> float**: Calculates and returns the minimum volume capacity of the box based on its dimensions and fill constraints.
  - **max_volume() -> float**: Calculates and returns the maximum volume capacity, ensuring packing remains within acceptable limits.

- **Purpose**:
  - **Defines Box Characteristics**: Provides detailed specifications for each box type, including physical constraints and metadata, which guides the packing process to select the right box for each order.

- **Relationships**:
  - **Created by BoxInputReader**: `BoxDefinition` instances are loaded and created by `BoxInputReader`, making them available to the `System` and `Packer` for use in packing strategies.

---

### 11. OrderManager

- **Methods**:
  - **sortOrdersByVolumeAndDimension() -> void**: Sorts the list of orders by volume and dimension to optimize packing efficiency, typically organizing larger items or orders first.

- **Purpose**:
  - **Manages Order Sorting**: Prepares orders for packing by sorting them according to volume and dimension, improving space utilization and packing efficiency.

---

### 12. Algorithm Interface

- **Methods**:
  - **DoesFit(box: Box, item: Product) -> bool**: Determines if a product can fit within a given box based on dimensions and other constraints.
  - **PlaceItem(box: Box, item: Product) -> void**: Places a product inside a box, assuming it fits, following specific packing rules.

- **Purpose**:
  - **Defines Standard Packing Operations**: Sets a standardized approach for packing algorithms, allowing for consistent and interchangeable packing strategies across different implementations.

---

### 13. BestFitDecreasing (Implements Algorithm)

- **Implements Methods from Algorithm**:
  - **DoesFit(box: Box, item: Product) -> bool**: Implements specific logic to check if a product fits within a box, optimized according to the best-fit decreasing strategy.
  - **PlaceItem(box: Box, item: Product) -> void**: Places items using a best-fit decreasing approach, filling the box in a way that maximizes space efficiency.

- **Relationships**:
  - **Implements Algorithm Interface**: Follows the `Algorithm` interface to provide a best-fit decreasing packing strategy, ensuring it can be swapped out with other strategies if needed.

---

### 14. Packer

- **Attributes**:
  - **positions**: A list of `Position` instances that keeps track of where each item is placed within the box, including orientation and coordinates.
  - **box**: The `Box` currently being packed. This is the container where all products are placed, with attributes like layers and fill capacity.

- **Methods**:
  - **initial_box_selection(products: list[Product], boxes: list[Box]) -> Box**: Selects an initial box for packing based on product and box attributes.
  - **volume_check, weight_check, dimension_check**: These methods verify that a set of products can fit within the box’s volume, weight, and dimension constraints.
  - **add_product(product: Product) -> bool**: Adds a product to the box if it meets all requirements, updating the box’s contents.
  - **reposition(product: Product) -> void**: Adjusts the position of a product within the box for optimal arrangement.
  - **initializeLayer, placeItemBySize, placeItemByAlgorithm**: Methods that organize the products within the box using various strategies, such as arranging items by size or algorithm-defined rules.
  - **processRemainingItems()**, **finalizePacking()**: Completes the packing operation, handling any remaining items and finalizing the arrangement within the box.

- **Relationships**:
  - **Uses Algorithm Interface**: `Packer` relies on an algorithm to determine placement strategies, making use of `DoesFit` and `PlaceItem` methods from the `Algorithm` interface.
  - **Uses Box for Storage**: Works directly with `Box` instances to place products within layers and manage available space during the packing process.


