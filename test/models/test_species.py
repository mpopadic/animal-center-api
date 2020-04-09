import unittest
from models import Species

from app import create_test_app
from database import db


class TestSpecies(unittest.TestCase):

    def setUp(self):
        create_test_app()
        db.create_all()

    def test_add_species(self):
        test_case = {'name': 'Max', 'description': 'brave dog', 'price' : 44}
        new_species = Species.add_species(_name=test_case['name'],
                                          _description=test_case['description'],
                                          _price=test_case['price'])
        self.assertEqual(new_species.name, test_case['name'])
        self.assertEqual(new_species.description, test_case['description'])
        self.assertEqual(new_species.price, test_case['price'])

        s = Species.query.filter_by(id=new_species.id).first()
        self.assertIsNot(s, None)
        self.assertEqual(s.name, test_case['name'])
        self.assertEqual(s.description, test_case['description'])
        self.assertEqual(s.price, test_case['price'])

    def test_add_species_type_error(self):
        test_case = {'name': 'Max', 'description': 4, 'price' : 44}
        self.assertRaises(TypeError,
                          Species.add_species,
                          _name=test_case['name'],
                          _description=test_case['description'],
                          _price=test_case['price'])

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()