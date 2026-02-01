from PIL.ImageQt import QPixmap  # For converting images to a Qt-compatible format.
from PyQt6.QtWidgets import (  # Import necessary PyQt widgets.
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QFrame, QListWidget, QMessageBox
)
from PyQt6.QtCore import Qt  # Core module for alignment and event handling.
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas  # For embedding Matplotlib in PyQt.
from PyQt6.QtWidgets import QGraphicsDropShadowEffect  # For adding shadow effects to widgets.
from PyQt6.QtGui import QColor, QGuiApplication  # To define colors for UI elements.
import os
from PyQt6.QtWidgets import QSizePolicy



os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

# Define a reusable drop shadow effect to style widgets.
shadow = QGraphicsDropShadowEffect()
shadow.setBlurRadius(15)  # Sets the blur radius for the shadow.
shadow.setXOffset(3)  # Horizontal offset of the shadow.
shadow.setYOffset(3)  # Vertical offset of the shadow.
shadow.setColor(QColor(0, 0, 0, 80))  # Shadow color with transparency.

from visualization.painter import Painter
from visualization.csv_reader import Reader

class OrderVisualizer(QMainWindow):
    """Main application class for visualizing orders and boxes."""


    def __init__(self, csv_file_path=None):
        super().__init__()
        self.csv_file_path = csv_file_path  # Optional file path for loading orders.
        self.Reader = Reader()  # Create an instance of the Reader to load CSV data.
        self.orders = []  # Initialize the list of orders.
        self.current_order_index = 0  # Index of the currently selected order.
        self.current_box_index = 0  # Index of the currently selected box.
        
        self.canvas = None  # Placeholder for the Matplotlib canvas.
        self.styles = ['default.css', 'protanopia_deuteranopia.css', 'tritanopia.css']  # List of available stylesheets.
        self.current_style_index = 0  # Index of the currently active stylesheet.
        
        self.reset_item()

        self.init_ui()  # Initialize the user interface.

        if self.csv_file_path:  # If a CSV file is provided, load orders from it.
            self.load_orders_from_file()

    def init_ui(self):
        self.setWindowTitle("Order Information")  # Set the title of the window.
        self.central_widget = QWidget()  # Create the central widget for the main window.
        self.setCentralWidget(self.central_widget)  # Assign it as the central widget.

        self.load_stylesheet("visualization/stylesheet/default.css")  # Load the default stylesheet.

        # Created the main vertical layout for the window.
        main_vertical_layout = QVBoxLayout(self.central_widget)
        main_vertical_layout.setSpacing(10)  # Spacing between widgets.
        main_vertical_layout.setContentsMargins(10, 10, 10, 10)  # Margins for the layout.
        main_vertical_layout.setObjectName('main_vertical_layout')  # Set object name for styling/debugging.
        
        
        ####################################################################T Top
        
        # Created the logo label to display the application logo in the top-left corner
        self.logo_label = QLabel()
        self.logo_label.setObjectName('logo_label')  # Assigned an object name for styling and debugging
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-aligned the logo within the label

        # Loaded and scaled the logo image to fit nicely within the layout
        pixmap = QPixmap("visualization/stylesheet/herbalife-new-logo-transparent.png")  # Loaded the logo image
        pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)  # Scaled the image
        self.logo_label.setPixmap(pixmap)  # Set the scaled image as the content of the logo label

        # Set fixed dimensions for the logo label to maintain consistent appearance
        self.logo_label.setFixedHeight(90)
        self.logo_label.setFixedWidth(90)  # Ensured both dimensions are explicitly set
        self.logo_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)  # Prevented resizing for a clean layout

        # Added an event to the logo for switching stylesheets on click
        self.logo_label.mousePressEvent = self.switch_stylesheet  # Bound the mouse press event to switch stylesheets

        # Created a label to display the current order information at the top of the interface
        self.order_info_top = QLabel("Order: NR XXXXXXX")  # Added placeholder text for the order number
        self.order_info_top.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-aligned the text for a balanced look
        self.order_info_top.setObjectName("order_info_top")  # Assigned an object name for easy styling
        self.order_info_top.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Allowed horizontal expansion while fixing the height

        # Organized the logo and order info label into a horizontal layout
        top_layout = QHBoxLayout()
        top_layout.setObjectName("top_layout")  # Assigned an object name for debugging and styling
        top_layout.setSpacing(10)  # Added some spacing between the logo and the order info label
        top_layout.addWidget(self.logo_label)  # Added the logo label to the layout
        top_layout.addWidget(self.order_info_top, stretch=1)  # Added the order info label and allowed it to stretch horizontally

        # Applied shadow effects to the labels for a polished, modern look
        self.apply_shadow(self.order_info_top)  # Added a shadow effect to the order info label
        self.apply_shadow(self.logo_label)  # Added a shadow effect to the logo label

        # Added the completed top layout to the main vertical layout of the application
        main_vertical_layout.addLayout(top_layout)
        
        ####################################################################
    

        #####################################################################
        # Main horizontal layout for left and right panels
        #####################################################################
        main_layout = QHBoxLayout()
        main_layout.setSpacing(10)  # Spacing between widgets
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for a clean layout
        main_vertical_layout.addLayout(main_layout)

        #####################################################################
        # Left Panel for Controls and Information
        #####################################################################
        left_panel = QVBoxLayout()
        left_frame = QFrame()  # Frame to contain the left panel
        left_frame.setObjectName("left_frame")  # Object name for styling/debugging
        left_frame.setFrameShape(QFrame.Shape.Box)  # Set a box shape for the frame
        left_frame.setLayout(left_panel)  # Assign the left panel layout to the frame
        main_layout.addWidget(left_frame, stretch=1)  # Add the frame to the main layout with stretch factor
        self.apply_shadow(left_frame)  # Apply shadow effect to the frame


        #####################################################################
        # Order Selection Section
        #####################################################################
        order_selection_frame = QFrame()
        order_selection_frame.setObjectName("order_selection_frame")  # Object name for styling/debugging
        order_selection_frame.setFrameShape(QFrame.Shape.Box)  # Box frame for the selection section
        order_selection_layout = QVBoxLayout(order_selection_frame)  # Create a layout for the section
        left_panel.addWidget(order_selection_frame)  # Add the selection frame to the left panel

        # Add a label for the order selection list
        order_list_label = QLabel("Order Selection")
        order_list_label.setObjectName("order_list_label")  # Object name for styling/debugging.
        order_list_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align the label text.
        order_selection_layout.addWidget(order_list_label)  # Add the label to the selection layout.

        # Create a list widget to display orders
        self.order_listbox = QListWidget()
        self.order_listbox.setObjectName("order_listbox")  # Object name for styling/debugging.
        self.order_listbox.itemSelectionChanged.connect(self.select_order)  # Connect selection changes to a method.
        order_selection_layout.addWidget(self.order_listbox)  # Add the list widget to the layout.

        # Navigation buttons for order selection
        nav_buttons_layout = QHBoxLayout()  # Create a horizontal layout for navigation buttons
        prev_button = QPushButton("Previous")  # Button to navigate to the previous order
        prev_button.clicked.connect(self.previous_order)  # Connect the button click to the navigation method
        nav_buttons_layout.addWidget(prev_button)  # Add the button to the layout

        next_button = QPushButton("Next")  # Button to navigate to the next order
        next_button.clicked.connect(self.next_order)  # Connect the button click to the navigation method
        nav_buttons_layout.addWidget(next_button)  # Add the button to the layout
        order_selection_layout.addLayout(nav_buttons_layout)

        self.apply_shadow(order_selection_frame)  # Apply shadow effect to the order selection frame


        #####################################################################
        # Box Information Section
        #####################################################################
        box_info_frame = QFrame()
        box_info_frame.setObjectName("box_info_frame")  # Object name for styling/debugging
        box_info_frame.setFrameShape(QFrame.Shape.Box)  # Set the frame shape to a box
        box_info_layout = QVBoxLayout(box_info_frame)  # Create a vertical layout for the box information frame
        left_panel.addWidget(box_info_frame, stretch=1)  # Add the box information frame to the left panel with stretch factor

        # Add a label for the box information section
        self.box_info_label = QLabel("Box Information")  # Updated text for consistency
        self.box_info_label.setObjectName("box_info_label")  # Set object name for styling/debugging
        self.box_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align the text in the label
        self.box_info_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Allow width expansion
        box_info_layout.addWidget(self.box_info_label)  # Add the label to the layout

        # Add a display label for detailed box information
        self.box_info_display = QLabel()
        self.box_info_display.setObjectName("box_info_display")  # Set object name for styling/debugging
        self.box_info_display.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align the text in the label
        self.box_info_display.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Allow both width and height to expand
        self.box_info_display.setMinimumHeight(80)  # Ensure enough space for content
        box_info_layout.addWidget(self.box_info_display)  # Add the label to the layout

        self.apply_shadow(box_info_frame)  # Apply shadow effect to the frame



        #####################################################################
        # Order Information Section
        #####################################################################
        
        order_info_frame = QFrame()
        order_info_frame.setObjectName("order_info_frame")  # Set object name for styling/debugging
        order_info_frame.setFrameShape(QFrame.Shape.Box)  # Set the frame shape to a box
        order_info_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)  # Responsive sizing
        order_info_layout = QVBoxLayout(order_info_frame)  # Create a vertical layout for the order information frame
        left_panel.addWidget(order_info_frame, stretch=1)  # Add the order information frame to the left panel with stretch factor

        # Add a label for the order information section
        self.order_info_label = QLabel("Order Info")
        self.order_info_label.setObjectName("order_info_label")  # Set object name for styling/debugging
        self.order_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align the text in the label
        order_info_layout.addWidget(self.order_info_label)  # Add the label to the layout

        # Add a display label for detailed order information
        self.order_info_display = QLabel()
        self.order_info_display.setObjectName("order_info_display")  # Set object name for styling/debugging
        self.order_info_display.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center-align the text in the label
        self.order_info_display.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Responsive sizing
        order_info_layout.addWidget(self.order_info_display)  # Add the label to the layout

        self.apply_shadow(order_info_frame) 
                
        #####################################################################
        # Navigation Buttons for Box Info Section
        #####################################################################
        # Add box navigation buttons below box info
        box_nav_buttons_layout = QHBoxLayout()  # Create a horizontal layout for box navigation buttons
        box_nav_buttons_layout.setSpacing(10)  # Set spacing between buttons

        # Previous Box Button
        prev_box_button = QPushButton("Box ←")
        prev_box_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Allow horizontal expansion
        prev_box_button.setMinimumHeight(40)  # Set a minimum height for the button
        prev_box_button.setMinimumWidth(2)  # Adjust width to be visually proportional
        prev_box_button.clicked.connect(self.previous_box)  # Connect the button to the previous_box method
        box_nav_buttons_layout.addWidget(prev_box_button)

        # Next Box Button
        next_box_button = QPushButton("→ Box")
        next_box_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Allow horizontal expansion
        next_box_button.setMinimumHeight(40)  # Set a minimum height for the button
        next_box_button.setMinimumWidth(2)  # Adjust width to be visually proportional
        next_box_button.clicked.connect(self.next_box)  # Connect the button to the next_box method
        box_nav_buttons_layout.addWidget(next_box_button)

        # Add box navigation buttons to the box_info_layout
        order_info_layout.addLayout(box_nav_buttons_layout)

        self.apply_shadow(prev_box_button)
        self.apply_shadow(next_box_button)

        
        #####################################################################
        # Plot Frame for Visualization
        #####################################################################

        # Plot Frame for Visualization
        self.plot_frame = QFrame()
        self.plot_frame.setObjectName("plot_frame")  # Object name for styling/debugging
        self.plot_layout = QVBoxLayout(self.plot_frame)  # Create a vertical layout for the plot frame
        self.plot_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Make the plot frame fully responsive
        main_layout.addWidget(self.plot_frame, stretch=3)  
                
        #####################################################################
        # Navigation Buttons for Item-Level Navigation
        #####################################################################

        # Add navigation buttons for item-level navigation
        item_nav_buttons_layout = QHBoxLayout()  # Create a horizontal layout for the navigation buttons
        item_nav_buttons_layout.setSpacing(10)  # Set spacing between buttons

        # Create a button to navigate back 10 items
        prev_item_x10_button = QPushButton("x10 ←")
        prev_item_x10_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Allow horizontal expansion
        prev_item_x10_button.setMinimumHeight(40)  # Set a minimum height for the button
        prev_item_x10_button.clicked.connect(lambda: self.update_item(-10))  # Connect the button click to update items
        item_nav_buttons_layout.addWidget(prev_item_x10_button)

        # Create a button to navigate back 1 item
        prev_item_button = QPushButton("←")
        prev_item_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Allow horizontal expansion
        prev_item_button.setMinimumHeight(40)  # Set a minimum height for the button
        prev_item_button.clicked.connect(lambda: self.update_item(-1))  # Connect the button click to update items
        item_nav_buttons_layout.addWidget(prev_item_button)

        # Create a button to navigate forward 1 item
        next_item_button = QPushButton("→")
        next_item_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Allow horizontal expansion
        next_item_button.setMinimumHeight(40)  # Set a minimum height for the button
        next_item_button.clicked.connect(lambda: self.update_item(1))  # Connect the button click to update items
        item_nav_buttons_layout.addWidget(next_item_button)

        # Create a button to navigate forward 10 items
        next_item_x10_button = QPushButton("→ x10")
        next_item_x10_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Allow horizontal expansion
        next_item_x10_button.setMinimumHeight(40)  # Set a minimum height for the button
        next_item_x10_button.clicked.connect(lambda: self.update_item(10))  # Connect the button click to update items
        item_nav_buttons_layout.addWidget(next_item_x10_button)

        box_info_layout.addLayout(item_nav_buttons_layout)  # Add the navigation buttons layout to the box info layout

        self.apply_shadow(prev_item_x10_button)
        self.apply_shadow(prev_item_button)
        self.apply_shadow(next_item_button)
        self.apply_shadow(next_item_x10_button)
        
        
        #####################################################################
        # Close Button
        #####################################################################

        # Create a close button to exit the application
        close_button_layout = QHBoxLayout()  # Create a horizontal layout for the close button
        close_button = QPushButton("Close")
        close_button.setObjectName("close_button")  # Set object name for styling/debugging
        close_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)  # Allow horizontal expansion
        close_button.setMinimumHeight(40)  # Set a minimum height for the button
        close_button.clicked.connect(self.close)  # Connect the button click to close the application
        close_button_layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)  # Center-align the button in the layout
        left_panel.addLayout(close_button_layout)  # Add the close button layout to the left panel

        self.apply_shadow(close_button)  # Apply shadow effect to the close button

        # Apply shadow effects to various frames and buttons.
        self.apply_shadow(box_info_frame)
        self.apply_shadow(self.plot_frame)

        self.showFullScreen()  # Maximize the application window to fill the screen.

    def update_order_list(self, order_ids=None):
        self.order_listbox.clear()
        if order_ids is None:
            order_ids = [order.get_order_id() for order in self.orders]
        self.order_listbox.addItems(order_ids)

    def load_orders_from_file(self):
        """Load orders from the selected CSV file."""
        try:
            self.orders = self.Reader.load_orders_from_csv(self.csv_file_path)
            self.update_order_list()
            self.update_display()
        except Exception as e:
            print(f"Error loading file: {e}")
            self.error_message(f"Failed to load orders from the file:\n{e}")

    def select_order(self):
        """Handle order selection from the list."""
        current_selection = self.order_listbox.currentRow()
        if current_selection >= 0:
            self.current_box_index = 0
            self.reset_item()
            self.current_order_index = current_selection
            self.update_display()

    def update_display(self):
        """Update the order and box information and the plot."""
        if not self.orders:
            self.error_message("No orders found.")
            return

        try:
            # Get the current order and box
            current_order = self.orders[self.current_order_index]
            current_box = current_order.boxes[self.current_box_index]  # Correctly fetch the current box

            # Update the top-level order information
            self.update_order_info_top(current_order, current_box, self.current_item_index, len(current_box.items))

            # Update order and box details with "Box X out of Y"
            total_boxes = len(current_order.boxes)  # Total boxes in the current order
            current_box_index_display = self.current_box_index + 1  # Convert to 1-based index
            total_items = sum(box.count_items() for box in current_order.boxes)  # Total items in the current order

            self.order_info_label.setText(f"Order Number: {current_order.get_order_id()}")
            self.order_info_display.setText(
                f"Box: {current_box_index_display} out of {total_boxes}\nItems: {total_items}"
            )

            self.box_info_label.setText(f"Box Number: {current_box.get_box_id()}")
            self.box_info_display.setText(
                f"Box Type: {current_box.get_box_name()}\nBox Items: {current_box.count_items()}"
            )

            # Update the plot
            self.update_plot(current_order, current_box)

        except Exception as e:
            self.error_message(f"Failed to update display: {e}")

    def update_plot(self, order, box):
        """Update the plot with the current order and box information."""
        painter = Painter(box)
        fig = painter.plotBoxAndItems(
            title=f"Order: {order.get_order_id()}, Box ID: {box.get_box_id()}",
            alpha=0.2,
            fontsize=10,
            limit=self.current_item_index,
            old_limit=self.previous_item_index
        )

        if self.canvas:
            self.plot_layout.removeWidget(self.canvas)
            self.canvas.setParent(None)

        self.canvas = FigureCanvas(fig)
        self.plot_layout.addWidget(self.canvas)
        self.canvas.draw()

    def reset_item(self):
        self.previous_item_index = 1
        self.current_item_index = 1

    def previous_order(self):
        """Navigate to the previous order."""
        if self.current_order_index > 0:
            self.current_order_index -= 1
            self.current_box_index = 0
            self.reset_item()
            self.update_display()

    def next_order(self):
        """Navigate to the next order."""
        if self.current_order_index < len(self.orders) - 1:
            self.current_order_index += 1
            self.current_box_index = 0
            self.reset_item()
            self.update_display()

    def error_message(self, message):
        """Show an error message dialog."""
        error_dialog = QMessageBox(self)
        error_dialog.setIcon(QMessageBox.Icon.Critical)
        error_dialog.setText(message)
        error_dialog.setWindowTitle("Error")
        error_dialog.exec()

    def update_item(self, delta):
        box = self.orders[self.current_order_index].boxes[self.current_box_index]
        self.current_item_index = max(1, min(self.current_item_index + delta, box.count_items()))
        old_item_index = self.current_item_index + 1 - abs(delta)

        if old_item_index != self.previous_item_index:
            self.previous_item_index = old_item_index
            self.update_display()

    def switch_stylesheet(self, event):
        """Switch stylesheets on logo click."""
        self.current_style_index = (self.current_style_index + 1) % len(self.styles)  # Cycle through styles
        stylesheet_path = f'visualization/stylesheet/{self.styles[self.current_style_index]}'
        self.load_stylesheet(stylesheet_path)

    def load_stylesheet(self, stylesheet_path):
        """Load a given stylesheet file."""
        try:
            with open(stylesheet_path, 'r') as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print(f"Stylesheet {stylesheet_path} not found!")

    def update_order_info_top(self, order, box, current_item_index, total_items):
        """Update the top order info dynamically."""
        item_title = f"({current_item_index} out of {total_items} items)"

        self.order_info_top.setText(
            f"Order {order.get_order_id()}:  {item_title}"
        )

    def apply_shadow(self, widget, blur_radius=15, x_offset=4, y_offset=4, color=(0, 0, 0, 80)):
        """
        Apply a drop shadow effect to a given widget.

        Args:
            widget (QWidget): The widget to apply the shadow effect to.
            blur_radius (int): The blur radius of the shadow.
            x_offset (int): The horizontal offset of the shadow.
            y_offset (int): The vertical offset of the shadow.
            color (tuple): The color of the shadow as (R, G, B, A).
        """
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blur_radius)
        shadow.setXOffset(x_offset)
        shadow.setYOffset(y_offset)
        shadow.setColor(QColor(*color))
        widget.setGraphicsEffect(shadow)

    def next_box(self):
        """Navigate to the next box in the current order."""
        try:
            # Fetch the current order
            current_order = self.orders[self.current_order_index]

            if self.current_box_index < len(current_order.boxes) - 1:  # Stay within the same order
                self.current_box_index += 1  # Increment the box index
                self.reset_item()
                self.update_display()  # Refresh the UI
            else:
                QMessageBox.information(self, "Box Navigation", "This is the last box in the current order.")
        except Exception as e:
            self.error_message(f"Error navigating to next box: {e}")

    def previous_box(self):
        """Navigate to the previous box in the current order."""
        try:
            # Check if there is a previous box in the current order
            if self.current_box_index > 0:  # Stay within the same order
                self.current_box_index -= 1  # Decrement the box index
                self.current_item_index = self.orders[self.current_order_index].boxes[self.current_box_index].count_items()
                self.previous_item_index = self.current_box_index
                self.update_display()  # Refresh the UI
            else:
                QMessageBox.information(self, "Box Navigation", "This is the first box in the current order.")
        except Exception as e:
            self.error_message(f"Error navigating to previous box: {e}")
            
            
     
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:  
            self.close()  
                



if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    # Create a QApplication instance before any PyQt objects.
    app = QApplication(sys.argv)

    # Instantiate your main window.
    main_window = OrderVisualizer()
    main_window.show()

    # Start the application event loop.
    sys.exit(app.exec())

