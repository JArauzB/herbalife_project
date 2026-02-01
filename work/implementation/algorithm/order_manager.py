from multiprocessing import Pool
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import threading
from .order_input_reader import OrderInputReader
from .product_input_reader import ProductInputReader
from .order import Order
from .product import Product

class OrderManager:
    """
    Manages the processing and organization of orders in the packing system.
    This class serves as a central coordinator for order processing, handling
    both order data loading and product information management.

    The manager performs these key functions:
    1. Loads order data from CSV files
    2. Loads product definitions
    3. Groups orders by order number
    4. Creates Order objects with associated products
    5. Manages parallel processing of orders

    Attributes:
        orderline_file_path (str): Path to the order lines CSV file
        product_file_path (str): Path to the product definitions CSV file
        order_input_reader (OrderInputReader): Singleton reader for orders
        product_input_reader (ProductInputReader): Singleton reader for products
        orders (List[Order]): List of processed orders

    Key Features:
        - Multi-processing support for order processing
        - Automatic file path resolution
        - Error handling for missing products
        - Order grouping and organization
        - Product-to-order association
    """

    def __init__(self, orderline_file_path='./data/orderline_definitions.csv', 
                 product_file_path='./data/product_definitions.csv'):
        """
        Initializes the OrderManager with file paths for data sources.

        Args:
            orderline_file_path (str): Path to order lines CSV file
            product_file_path (str): Path to product definitions CSV file

        Note:
            - Paths are relative to the module location
            - Creates singleton reader instances
            - Initializes empty order list
        """
        self.orderline_file_path = orderline_file_path
        self.product_file_path = product_file_path
        self.order_input_reader = OrderInputReader()
        self.product_input_reader = ProductInputReader()
        self.orders = []
    
    def reset(self, orderline_file_path, product_file_path):
        """
        Resets the manager state with new file paths.
        Used when processing multiple batches or restarting.

        Args:
            orderline_file_path (str): New path to order lines file
            product_file_path (str): New path to product definitions file

        Note:
            - Clears existing orders
            - Updates file paths
            - Prepares for new processing cycle
        """
        self.orderline_file_path = orderline_file_path
        self.product_file_path = product_file_path
        self.orders = []

    def process_orders(self):
        """
        Processes all orders using parallel processing for efficiency.
        
        The processing workflow:
        1. Reset manager state
        2. Load order data
        3. Group orders by order number
        4. Process orders in parallel
        5. Collect and return results

        Returns:
            List[Order]: List of processed orders

        Note:
            - Uses multiprocessing for performance
            - Preserves one CPU core for system
            - Handles order grouping automatically
            - Returns fully processed orders
        """
        self.reset(self.orderline_file_path, self.product_file_path)

        loaded_orders = self.load_orders()
        grouped_orders = self.group_by_order(loaded_orders)

        # Determine number of processes
        num_cores = os.cpu_count()
        num_processes = max(1, num_cores - 1)  # Leave one core free

        # Prepare data for multiprocessing
        grouped_orders_list = list(grouped_orders.values())

        # Use multiprocessing to process orders in parallel
        with Pool(processes=num_processes) as pool:
            results = pool.map(self.create_order, grouped_orders_list)

        self.orders = results
        return self.orders

    def load_products(self):
        """
        Loads product definitions from the product file.
        
        Returns:
            List[Dict]: List of product definitions

        Note:
            - Uses ProductInputReader singleton
            - Caches product data
            - Required for order processing
            - Contains complete product specifications
        """
        self.product_input_reader.read_csv(self.product_file_path)
        products = self.product_input_reader.get_data()

        return products
    
    def load_orders(self):
        """
        Loads order data from the order lines file.
        
        Returns:
            List[Dict]: List of order line entries

        Note:
            - Uses OrderInputReader singleton
            - Caches order data
            - Contains raw order information
            - Prepared for grouping and processing
        """
        self.order_input_reader.read_csv(self.orderline_file_path)
        orders = self.order_input_reader.get_data()

        return orders

    def group_by_order(self, data):
        """
        Groups order lines by order number for efficient processing.
        
        Args:
            data (List[Dict]): Raw order line data

        Returns:
            Dict[str, List[Dict]]: Orders grouped by order number

        Note:
            - Critical for order organization
            - Prepares for parallel processing
            - Maintains order integrity
            - Groups related items together
        """
        grouped_data = {}

        for row in data:
            order_id = row['Ordernr']
            if order_id not in grouped_data:
                grouped_data[order_id] = []
            grouped_data[order_id].append(row)

        return grouped_data

    def create_order(self, order):
        """
        Creates an Order object from grouped order lines.
        
        Args:
            order (List[Dict]): Group of order lines for one order

        Returns:
            Order: Fully initialized order with products

        Note:
            - Loads required product data
            - Handles quantity multiplication
            - Validates product existence
            - Creates Product instances
            - Sets order metadata
            - Manages error cases
        """
        products_data = self.load_products()

        order_number = order[0]['Ordernr']
        date_time = order[0]['Date']
        items = []

        for item in order:
            try:
                product_data = next((product for product in products_data if product['ID'] == item['ID']), None)
                product_id = item['ID']

                if not product_data:
                    raise ValueError(f"Product ID {product_id} not found in product data.")
                picked_quantity = int(item.get('Picked'))
                for _ in range(picked_quantity):
                    product = Product(
                        width=float(product_data['Width']),
                        height=float(product_data['Height']),
                        length=float(product_data['Length']),
                        weight=float(product_data['Weight']),
                        fit_ratio=float(product_data['Fit ratio']),
                        item=product_id,
                        location=item['Location']
                    )
                    items.append(product)

            except ValueError as e:
                print(f"Error creating product for item {item}: {e}")
                continue

        order = Order(order_number, date_time, items)
        order.order_items()

        return order
