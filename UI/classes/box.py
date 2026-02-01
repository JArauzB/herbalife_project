class Box:
    def __init__(self, box_id):
        self.box_id = box_id
        self.items = []  # List to hold Item objects

    def add_item(self, item):
        self.items.append(item)

    def __repr__(self):
        return f"Box(id={self.box_id}, items={self.items})"