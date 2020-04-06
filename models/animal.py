from database import db


class Animal(db.Model):
    __tablename__ = "animals"

    id = db.Column(db.Integer, primary_key=True)
    center_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    species = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(120), nullable=True)

    def __init__(self, center_id, name, age, species, price=None, description=None):
        self.center_id = center_id
        self.name = name
        self.age = age
        self.species = species
        self.price = price
        self.description = description



