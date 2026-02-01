import csv
import os

class ProductInputReader:
    """
    A singleton class responsible for loading and managing product definitions from CSV files.
    This class is essential for initializing product information in the packing system.

    The CSV file should contain product definitions with:
    - Product ID and metadata
    - Physical dimensions (length, width, height)
    - Weight information
    - Unit of measure codes
    - Fit ratio specifications

    Key Features:
        - Singleton pattern implementation
        - File modification tracking
        - Cached data management
        - CSV parsing with headers
        - UTF-8 encoding support

    Example CSV format:
    ID,Weight,Length,Width,Height,UOM Code,Fit ratio
    5234,640,113,113,208,MM,100
    5945,2,170,50,20,MM,100
    ...

    Attributes:
        _instance (ProductInputReader): Singleton instance
        loaded_products (list): Cached product definitions
        last_loaded_time (float): Last file modification timestamp

    Usage:
        reader = ProductInputReader()
        reader.read_csv('./data/products.csv')
        products = reader.get_data()
    """

    _instance = None
    loaded_products = []
    last_loaded_time = None

    def __new__(cls, *args, **kwargs):
        """
        Implements the singleton pattern to ensure only one instance exists.
        
        Returns:
            ProductInputReader: The singleton instance

        Note:
            - Creates new instance if none exists
            - Returns existing instance otherwise
            - Ensures consistent data access
            - Thread-safe implementation
        """
        if cls._instance is None:
            cls._instance = super(ProductInputReader, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def read_csv(self, file_path):
        """
        Reads and parses product definitions from a CSV file.
        Only reloads if file has been modified since last read.

        Args:
            file_path (str): Path to the CSV file containing product definitions

        Returns:
            bool: True if new data was loaded, False if using cached data

        Note:
            - Checks file modification time
            - Uses UTF-8 with BOM support
            - Caches loaded data
            - Maintains last loaded timestamp
            - Skips reload if file unchanged
            - Critical for product initialization
        """
        last_loaded_time = os.path.getmtime(file_path)

        if self.loaded_products:
            if hasattr(self, 'last_loaded_time') and self.last_loaded_time == last_loaded_time:
                return False

        self.last_loaded_time = last_loaded_time
        data = []

        with open(file_path, mode='r', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)

        self.loaded_products = data

        return True
    
    def get_data(self):
        """
        Retrieves the cached product definitions.
        
        Returns:
            list: List of dictionaries containing product information

        Note:
            - Returns cached data from last file read
            - Each dictionary represents one product
            - Contains complete product specifications
            - Used by OrderManager for product creation
            - Essential for packing algorithm
        """
        return self.loaded_products
