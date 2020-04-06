import uuid


class Species:

    def __init__(self, name, description, price):
        self.id = uuid.uuid4()
        self.name = name
        self.description = description
        self.price = price