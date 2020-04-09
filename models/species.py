from database import db


class Species(db.Model):
    __tablename__ = "species"

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column('name', db.String(50))
    _description = db.Column('description', db.String(120))
    _price = db.Column('price', db.Integer)
    animals = db.relationship("Animal", backref="origin")

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError('name must be a string')
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError('description must be a string')
        self._description = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, int) or type(value) is not int:
            raise TypeError('price must be a int')
        self._price = value

    @staticmethod
    def json(species):
        return {'id': species.id, 'name': species.name, 'description': species.description, 'price': species.price}

    @staticmethod
    def get_all_species():
        species = Species.query.all()
        return ['{0}s - {1}'.format(s.name, len(s.animals)) for s in species]

    @staticmethod
    def get_species_by_id(_id):
        species = Species.query.filter_by(id=_id).first()
        if species:
            return Species.json(species)
        else:
            return {}

    @staticmethod
    def add_species(_name, _description, _price):
        new_species = Species(_name, _description, _price)
        db.session.add(new_species)
        db.session.commit()
        return new_species

    @staticmethod
    def is_valid_object(species):
        return species.get("name", None) is not None \
               and species.get("description", None) is not None\
               and species.get("price", None) is not None
