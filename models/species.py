from database import db


class Species(db.Model):
    __tablename__ = "species"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(120))
    price = db.Column(db.Integer)
    animals = db.relationship("Animal", backref="origin")

    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price

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

    @staticmethod
    def is_valid_object(species):
        return species.get("name", None) is not None \
               and species.get("description", None) is not None\
               and species.get("price", None) is not None
