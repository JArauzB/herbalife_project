from multiprocessing import Lock, Pool, Manager
import os
import csv
from math import ceil
import time
from .packer import Packer
from .order_manager import OrderManager
from .box_input_reader import BoxInputReader

class System:
    """
    Coordinates the overall packing system operation and manages the packing process.
    This class serves as the main entry point for the packing algorithm, handling
    file I/O, order processing, and result generation.

    The system handles:
    - Order data loading and processing
    - Product definition management
    - Box configuration loading
    - Multi-threaded packing execution
    - Result generation and export
    - Progress tracking and reporting

    Key Features:
        - Parallel order processing
        - Progress monitoring
        - CSV result generation
        - Resource management
        - Performance optimization
        - Error handling
    """

    def __init__(self, output_file='./data/output_temp.csv'):
        """
        Initializes the packing system with output configuration.

        Args:
            output_file (str): Path for results CSV file

        Note:
            - Creates OrderManager instance
            - Prepares output handling
            - Sets up system state
        """
        self.order_manager = OrderManager()
        self.output_file = output_file

    def start_processing(self, orderline_file_path, product_file_path):
        """
        Initiates the packing process with specified input files.
        Manages the complete packing workflow from data loading to result export.

        Args:
            orderline_file_path (str): Path to order data CSV
            product_file_path (str): Path to product definitions CSV

        Note:
            - Adjusts paths for module location
            - Loads box definitions
            - Manages parallel processing
            - Tracks progress
            - Handles resource allocation
            - Reports execution time
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        adjusted_orderline_file_path = os.path.join(current_dir, orderline_file_path)
        adjusted_product_file_path = os.path.join(current_dir, product_file_path)
        box_file_path = os.path.join(current_dir, './data/box_definition.json')

        self.order_manager.reset(adjusted_orderline_file_path, adjusted_product_file_path)

        # Process all orders
        start_time = time.time()
        processed_orders = self.order_manager.process_orders()

        self.orders = sorted(processed_orders, key=lambda x: len(x.items), reverse=True)
        end_time = time.time()

        print(f"Processing + sorting time: {end_time - start_time} seconds for {len(self.orders)} orders with {sum(len(order.items) for order in self.orders)} orderlines")

        # Process all available boxes
        self.boxes = BoxInputReader.load_boxes(box_file_path)

        # Determine number of processes
        num_cores = os.cpu_count()
        num_processes = max(1, num_cores - 1)  # Leave one core free

        self.order_count = len(self.orders)
        step_size = min(self.order_count, num_processes * 2)
        chunked_orders = [self.orders[i::step_size] for i in range(step_size)]

        self.total_working_time = 0

        # Manager for shared state
        with Manager() as manager:
            progress_counter = manager.Value('i', 0)  # Shared counter initialized to 0
            lock = manager.Lock()  # Use Manager's Lock for multiprocessing

            args = [(chunk, self.boxes, progress_counter, self.order_count, lock) for chunk in chunked_orders]

            with Pool(processes=min(num_processes, self.order_count)) as pool:
                results = pool.starmap(self.pack_orders_in_chunk, args)

                packers = [result[0] for result in results]
                times = [result[1] for result in results]

            self.packers = packers
        
            print(f"Total working time: {sum(times)} seconds")

        self.export_packed_box()

    @staticmethod
    def pack_orders_in_chunk(orders, boxes, progress_counter, total_orders, lock):
        """
        Processes a subset of orders in parallel.
        Part of the multi-threading optimization strategy.

        Args:
            orders (list): Orders to process
            boxes (list): Available box definitions
            progress_counter (Value): Shared progress tracking
            total_orders (int): Total order count
            lock (Lock): Thread synchronization lock

        Note:
            - Thread-safe progress updates
            - Visual progress indication
            - Performance timing
            - Resource management
        """
        start_time = time.time()
        packer = Packer()

        for order in orders:
            packer.pack_order(order, boxes)

            with lock:  # Ensure thread-safe updates
                progress_counter.value += 1

            progress = progress_counter.value / total_orders
            bar_length = 40
            block = int(round(bar_length * progress))
            bar = '#' * block + '-' * (bar_length - block)
            num_digits = len(str(total_orders))
            print(f"\rProcessing order {progress_counter.value:{num_digits}} out of {total_orders}...\t[{bar}] {progress * 100:.2f}%", end='')

        end_time = time.time()

        processing_time = end_time - start_time

        return packer, processing_time

    def export_packed_box(self):
        """
        Exports packing results to CSV format.
        Generates detailed placement information for all packed items.

        Note:
            - Creates standardized output
            - Includes all packing details
            - Handles file writing
            - Uses UTF-8 encoding
            - Includes headers
            - Manages file paths
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(current_dir, self.output_file)

        # Writing the data to a CSV file
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)

            writer.writerow([
                "Order ID",
                "Box ID",
                "Box Type",
                "Box Width",
                "Box Height",
                "Box Depth",
                "Item Name",
                "Item Width",
                "Item Height",
                "Item Depth",
                "Item Position X",
                "Item Position Y",
                "Item Position Z"
            ])

            # Write each row of data
            for packer in self.packers:
                for entry in packer.get_packer_csv_result().split('\n'):
                    if entry.strip():
                        fields = entry.split(',')
                        writer.writerow(fields)
