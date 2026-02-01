import logging
import os
import time

from PyQt6.QtWidgets import QApplication

from algorithm.system import System
from visualization.order_visualizer import OrderVisualizer
import sys

logging.basicConfig(
    level=logging.CRITICAL, # Set the logging level, options: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # Stream logs to console
)
logging.basicConfig(level=logging.DEBUG)

class Main:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        # self.orders_file = './data/test_orders_temp.csv'
        # self.orders_file = './data/orders.csv'
        self.orders_file = './data/orderline_definitions.csv'
        self.product_file = './data/product_definitions.csv'

        # self.output_file = './algorithm/data/output.csv'
        self.output_file = './algorithm/data/output_temp.csv'
        # self.output_file = './algorithm/data/output_orderline_definitions_retry_2.csv'

        self.demo_orders_file = './data/orders.csv'
        self.demo_product_file = './data/demo_products.csv'
        self.demo_product_file = './data/product_definitions.csv'
        self.demo_output_file = './data/demo_output.csv'

        self.algorithm_output_file = '.' + self.output_file.split('algorithm')[1]

    def start(self, algorithm, visualization, demo):
        if (algorithm):
            startTime = time.time()
            system = System(self.demo_output_file if demo else self.algorithm_output_file)
            system.start_processing(self.demo_orders_file if demo else self.orders_file, self.demo_product_file if demo else self.product_file)
            endTime = time.time()

            total_boxes = sum(len(orderResult.boxes) for packer in system.packers for orderResult in packer.orderResults)
            orderlines = sum(len(orderResult.order.packed_items) for packer in system.packers for orderResult in packer.orderResults)
            print(f"\nProcessing time: {endTime - startTime} seconds for {len(system.orders)} orders, {total_boxes} boxes with {orderlines} orderlines")

        if visualization:
            os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"  
            app = QApplication(sys.argv)
            visualizer = OrderVisualizer(os.path.join(self.current_dir, self.output_file))
            visualizer.show()
            sys.exit(app.exec())


if __name__ == '__main__':
    # Default to demo mode if no arguments are provided
    mode = int(sys.argv[1]) if len(sys.argv) > 1 else 3

    if mode == 0:
        Main().start(True, False, False)
    elif mode == 1:
        Main().start(False, True, False)
    elif mode == 2:
        Main().start(True, True, False)
    elif mode == 3:
        Main().start(True, True, True)