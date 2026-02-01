import logging

from .fragment import Fragment
from .position import Position
from .rotation_type import RotationType

def check_collision(new_position, existing_coordinates):
    new_x, new_y, new_z = new_position.get_coordinates()
    new_width, new_height, new_length = new_position.get_dimensions()

    for coord in existing_coordinates:
        product_id, x, y, z, width, height, length = coord
        if (
            new_x < x + width and new_x + new_width > x and
            new_y < y + height and new_y + new_height > y and
            new_z < z + length and new_z + new_length > z
        ):
            logging.debug(f"Collision detected between new product {new_position.get_product().item} "
                          f"and product {product_id} at coordinates {x, y, z}.")
            return True

    logging.debug(f"No collision detected for product {new_position.get_product().item}.")
    return False

class LayerResult:
    """
    Represents a layer of products within a box, managing product placement and space optimization.
    This class is crucial for the 3D bin packing algorithm as it handles the actual placement logic
    for products within a single horizontal layer.

    The class uses a sophisticated space management system that:
    1. Tracks remaining spaces as fragments
    2. Attempts to fit products in the most optimal way
    3. Splits spaces around placed products to maximize utilization

    Attributes:
        box (BoxDefinition): The box containing this layer
        base_height (float): Starting height of this layer from box bottom
        layer_height (float): Current height of the layer
        remaining_height (float): Available height above this layer
        remaining_width (float): Available width in the layer
        remaining_length (float): Available length in the layer
        remaining_spaces (List[Fragment]): List of available spaces for product placement
        positions (List[Position]): List of placed products with their positions
        last_product (str): ID of the last product placed (for optimization)
        last_space (Fragment): Last space used (for optimization)

    Key Algorithms:
        - Space Splitting: When a product is placed, the surrounding space is split into
          up to 6 new fragments (front, back, left, right, top, bottom)
        - Best Fit Selection: Products are placed in spaces that minimize fragmentation
        - Collision Detection: Ensures products don't overlap with existing placements
    """

    def __init__(self, box, base_height=0):
        """
        Initializes a new layer within a box.

        Args:
            box (BoxDefinition): The box containing this layer
            base_height (float): Starting height of this layer from box bottom in cm

        Note:
            The layer initially creates one large fragment representing all available space.
            This space will be subdivided as products are placed.
        """
        self.box = box
        self.base_height = base_height
        self.layer_height = 0
        self.remaining_height = box.height - base_height
        self.remaining_width = box.width
        self.remaining_length = box.length
        self.remaining_spaces = [Fragment(0, base_height, 0, box.width, box.height - base_height, box.length)]
        self.positions = []

        self.last_product = None
        self.last_space = None

    def add_product(self, position, existing_coordinates, use_reverse_y = False):
        """
        Attempts to add a product to the layer using sophisticated placement algorithms.
        
        The method follows these steps:
        1. For each available space, try all possible rotations of the product
        2. Score each valid placement based on resulting fragmentation
        3. Select the placement that minimizes wasted space
        4. Update remaining spaces after successful placement

        Args:
            position (Position): Product and its initial position/rotation
            existing_coordinates (List[tuple]): Coordinates of already placed products
            use_reverse_y (bool): Whether to try placements from top to bottom

        Returns:
            bool: True if product was successfully placed, False otherwise

        Note:
            The algorithm prioritizes:
            - Minimizing fragmentation of remaining space
            - Maintaining stability through proper support
            - Efficient space utilization
        """
        logging.debug(f"Adding product {position.get_product().get_product_name()} {self.box.container_type} to layer")
        if self.box.container_type == "XXS":
            self.positions.append(position)
            return True

        best_fit = None
        best_fit_score = float('inf')
        best_position = None
        selected_space = None

        product = position.get_product()

        found_space = not self.last_space or not self.last_product or product.item != self.last_product
        list_of_spaces = sorted(self.remaining_spaces, key=lambda individual: not individual.new)

        if found_space:
            temp_spaces = []

            for space in list_of_spaces:
                if space.new:
                    space.new = False
                if space.volume() >= product.volume() and found_space:
                    temp_spaces.append(space)

                if not found_space:
                    found_space = space == self.last_space

            list_of_spaces = sorted(temp_spaces, key=lambda individual: (individual.z, individual.x), reverse=False)

        if self.last_space and self.last_product and product.item != self.last_product:
            if list_of_spaces.count(self.last_space) > 0:
                list_of_spaces.remove(self.last_space)
                self.last_space = None

        for space in sorted(list_of_spaces, key=lambda individual: individual.y, reverse=use_reverse_y):
            rotation = RotationType.initial_rotation(*(product.get_dimensions()))
            current_rotation = None

            if (best_position):
                break

            for _ in range(rotation.min_value(), rotation.max_value()):
                if not current_rotation:
                    current_rotation = rotation
                else:
                    current_rotation = current_rotation.next_rotation()

                rotated_width, rotated_height, rotated_length = current_rotation.adjust_dimensions(*(product.get_dimensions()))

                if (
                        rotated_width <= space.width and
                        rotated_length <= space.length and
                        rotated_height <= space.height
                ):
                    position.set_orientation(current_rotation)
                    position.set_coordinates(space.x, space.y, space.z)

                    # if True:
                    if not any(position.calculate_extending_point()[i] > self.box.get_box_dimensions()[i] for i in range(3)):
                        if (space.y + min(product.get_dimensions()) > self.box.height):
                            break

                        if check_collision(position, existing_coordinates):
                            continue

                        fragmentation = (space.width - rotated_width) * (space.length - rotated_length)
                        if fragmentation < best_fit_score:
                            best_position = position.copy()
                            best_fit_score = fragmentation
                            best_fit = current_rotation
                            selected_space = space

        if best_position and best_fit and selected_space:
            self.last_space = selected_space
            self.last_product = product.item
            best_position.set_orientation(best_fit)
            self.positions.append(best_position)
            self.update_remaining_spaces(best_position)
            return True

        return False


    def update_remaining_spaces(self, position):
        """
        Updates the available spaces after placing a product by splitting existing spaces.
        
        This is a critical method that maintains the space management system by:
        1. Identifying affected spaces that intersect with the new product
        2. Splitting those spaces into smaller fragments around the product
        3. Maintaining a list of usable spaces for future placements

        Args:
            position (Position): The position of the newly placed product

        Note:
            The splitting algorithm creates up to 6 new fragments per affected space:
            - Left and right of the product
            - In front and behind the product
            - Above and below the product
            Only fragments with positive dimensions are kept.
        """
        updated_spaces = []
        start_x, start_y, start_z = position.get_coordinates()

        for space in self.remaining_spaces:
            if (
                    start_x < space.x + space.width and
                    start_y < space.y + space.height and
                    start_z < space.z + space.length
            ):
                updated_spaces += self.split_space_around_product(space, position)
            else:
                updated_spaces.append(space)

        self.remaining_spaces = updated_spaces
        logging.debug(
            f"Updated remaining spaces after placing product {position.get_product().item}: {self.remaining_spaces}"
        )

    def split_space_around_product(self, space, position):
        fragments = []
        start_x, start_y, start_z = position.get_coordinates()
        end_x, end_y, end_z = position.calculate_extending_point()

        if (space.x <= start_x < space.x + space.width and space.x < end_x <= space.x + space.width) \
            and (space.y <= start_y < space.y + space.height and space.y < end_y <= space.y + space.height) \
            and (space.z <= start_z < space.z + space.length and space.z < end_z <= space.z + space.length):

            logging.debug("Splitting space")
            if space.x <= start_x < space.x + space.width:
                fragments.append(Fragment(space.x, space.y, space.z, start_x - space.x, space.height, space.length))
            if space.x < end_x <= space.x + space.width:
                fragments.append(Fragment(end_x, space.y, space.z, space.x + space.width - end_x, space.height, space.length))

            if space.y <= start_y < space.y + space.height:
                fragments.append(Fragment(space.x, space.y, space.z, space.width, start_y - space.y, space.length))
            if space.y < end_y <= space.y + space.height:
                fragments.append(Fragment(space.x, end_y, space.z, space.width, space.y + space.height - end_y, space.length))

            if space.z <= start_z < space.z + space.length:
                fragments.append(Fragment(space.x, space.y, space.z, space.width, space.height, start_z - space.z))
            if space.z < end_z <= space.z + space.length:
                fragments.append(Fragment(space.x, space.y, end_z, space.width, space.height, space.z + space.length - end_z))
        else:
            logging.debug("Not splitting space")
            fragments.append(space)

        logging.debug(f"Split space {space} around product {position.get_product().item}. Fragments: {fragments}")
        return fragments

    def find_fit_in_remaining_spaces(self, product, existing_coordinates):
        for space in self.remaining_spaces:
            for rotation in RotationType:
                width, height, length = rotation.adjust_dimensions(
                    product.width, product.height, product.length
                )
                if (
                        width <= space.width and
                        height <= space.height and
                        length <= space.length
                ):
                    position = Position(product, space.x, space.y, space.z, rotation)

                    if not check_collision(position, existing_coordinates):
                        self.update_remaining_spaces(position)
                        self.positions.append(position)
                        logging.debug(
                            f"Product {product.get_product_name()} placed in fragmented space. "
                            f"Coordinates: {position.get_coordinates()}."
                        )
                        return True
        return False

    def get_positions(self):
        return self.positions

    def get_product_coordinates(self):
        """
              Return a list of all products with their coordinates and dimensions.
        """
        return [(p.get_product().get_product_name(), *p.get_coordinates(), *p.get_dimensions()) for p in self.positions]
