import csv
import os

class OrderInputReader:
    """
    A singleton class responsible for reading and managing order data from CSV files.
    This class is essential for initializing order information in the packing system.

    The CSV file should contain order lines with:
    - Order identification (order number, date)
    - Product information (ID, location)
    - Quantity information (picked amount)
    - Box specifications (box name, type)
    - Weight information

    Key Features:
        - Singleton pattern implementation
        - File modification tracking
        - Cached data management
        - CSV parsing with headers
        - UTF-8 encoding support

    Example CSV format:
    Date,Ordernr,Boxnr,Picked,Location,Box Name,Weight,ID
    2024-02-09,6S04573613,13848903,1,05D27,XS,640,5234
    2024-02-09,6S04573613,13848903,1,12B24,XS,2,5945
    ...

    Attributes:
        _instance (OrderInputReader): Singleton instance
        loaded_orders (list): Cached order data
        last_loaded_time (float): Last file modification timestamp
    """

    _instance = None
    loaded_orders = []
    last_loaded_time = None

    def __new__(cls, *args, **kwargs):
        """
        Implements the singleton pattern to ensure only one instance exists.
        
        Returns:
            OrderInputReader: The singleton instance

        Note:
            - Creates new instance if none exists
            - Returns existing instance otherwise
            - Thread-safe implementation
        """
        if cls._instance is None:
            cls._instance = super(OrderInputReader, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def read_csv(self, file_path):
        """
        Reads and parses order data from a CSV file.
        Only reloads if file has been modified since last read.

        Args:
            file_path (str): Path to the CSV file containing order data

        Returns:
            bool: True if new data was loaded, False if using cached data

        Note:
            - Checks file modification time
            - Uses UTF-8 with BOM support
            - Caches loaded data
            - Maintains last loaded timestamp
            - Skips reload if file unchanged
        """
        last_loaded_time = os.path.getmtime(file_path)

        if self.loaded_orders:
            if hasattr(self, 'last_loaded_time') and self.last_loaded_time == last_loaded_time:
                return False
            
        self.last_loaded_time = last_loaded_time
        data = []

        with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)

        self.loaded_orders = data

        return True

    def get_data(self):
        """
        Retrieves the cached order data.
        
        Returns:
            list: List of dictionaries containing order information

        Note:
            - Returns cached data from last file read
            - Each dictionary represents one order line
            - No file reading in this method
            - Used by OrderManager for order processing
        """
        return self.loaded_orders
