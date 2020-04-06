import uuid


class Animal:

    def __init__(self, center_id, name, age, species, price=None, description=None):
        self.id = uuid.uuid4()
        self.center_id = center_id
        self.name = name
        self.age = age
        self.species = species
        self.price = price
        self.description = description



