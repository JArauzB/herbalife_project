# visualization/__init__.py
from .box import Box
from .csv_reader import Reader
from .item import Item
from .order import Order
from .painter import Painter

# Metadata
__version__ = '1.0.0'

# Expose a function to load modules, avoiding circular imports
__all__ = ['__version__']
