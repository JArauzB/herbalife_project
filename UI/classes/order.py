class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.boxes = []  # List to hold Box objects

    def add_box(self, box):
        self.boxes.append(box)

    def __repr__(self):
        return f"Order(id={self.order_id}, boxes={self.boxes})"
