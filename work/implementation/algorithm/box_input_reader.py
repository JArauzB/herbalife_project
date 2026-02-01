import json
import os
from .box_definition import BoxDefinition

class BoxInputReader:
    """
    A class responsible for loading and parsing box definitions from JSON configuration files.
    This class is crucial for initializing the available box types for the packing algorithm.

    The JSON file should contain an array of box definitions, each with:
    - Physical dimensions (length, height, width)
    - Weight constraints (weight, max_weight)
    - Descriptive information (description, container_type, remark)
    - Fill constraints (max_fill_percentage, min_fill_percentage)

    Key Features:
        - Static utility class (no instance required)
        - Path resolution relative to module location
        - Automatic conversion of JSON data to BoxDefinition objects
        - Default values for optional parameters

    Example JSON format:
    [
        {
            "length": 330,
            "height": 35,
            "width": 245,
            "weight": 30,
            "max_weight": 19970,
            "description": "Envelope",
            "container_type": "ENV",
            "remark": "Standard envelope",
            "max_fill_percentage": 80.0,
            "min_fill_percentage": 5.0
        },
        ...
    ]
    """

    @staticmethod
    def load_boxes(file_path: str = './data/box_definition.json') -> list:
        """
        Loads box definitions from a JSON file and converts them to BoxDefinition objects.

        Args:
            file_path (str): Path to the JSON file containing box definitions.
                           Defaults to './data/box_definition.json'

        Returns:
            list[BoxDefinition]: List of initialized box definition objects

        Note:
            - Paths are resolved relative to the module location
            - Missing optional values use defaults:
                * max_fill_percentage: 80.0
                * min_fill_percentage: 5.0
                * description: ''
                * container_type: ''
                * remark: ''
            - Required values must be present:
                * width, height, length
                * weight, max_weight

        Example:
            boxes = BoxInputReader.load_boxes()
            boxes = BoxInputReader.load_boxes('./custom/boxes.json')
        """
        adjusted_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_path)
        
        with open(adjusted_file_path, 'r') as file:
            data = json.load(file)
        
        boxes = []
        for item in data:
            box = BoxDefinition(
                width=item.get('width', 0),
                height=item.get('height', 0),
                length=item.get('length', 0),
                weight=item.get('weight', 0),
                max_weight=item.get('max_weight', 0),
                description=item.get('description', ''),
                container_type=item.get('container_type', ''),
                remark=item.get('remark', ''),
                max_fill_percentage=item.get('max_fill_percentage', 80.0),
                min_fill_percentage=item.get('min_fill_percentage', 5.0)
            )
            boxes.append(box)
        
        return boxes