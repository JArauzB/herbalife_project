from .box_definition import BoxDefinition
from .box_input_reader import BoxInputReader
from .box_result import BoxResult
from .fragment import Fragment
from .layer_result import LayerResult
from .order_input_reader import OrderInputReader
from .order_manager import OrderManager
from .order_result import OrderResult
from .order import Order
from .hello_world import HelloWorld
from .packer import Packer
from .position import Position
from .product_input_reader import ProductInputReader
from .product import Product
from .rotation_type import RotationType
from .system import System

# Package-level variable
__version__ = '1.0.0'

# Expose a function to load modules, avoiding circular imports
__all__ = ['__version__']