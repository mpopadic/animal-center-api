import unittest
from models import Center

from app import create_test_app
from database import db


class TestCenter(unittest.TestCase):

    def setUp(self):
        create_test_app()
        db.create_all()

    def test_add_center(self):
        test_case = {'login': 'User1', 'password': 'pass1', 'address' : 'address 1'}
        new_center = Center.add_center(_login=test_case['login'],
                                       _password=test_case['password'],
                                       _address=test_case['address'])
        self.assertEqual(new_center.login, test_case['login'])
        self.assertEqual(new_center.password, test_case['password'])
        self.assertEqual(new_center.address, test_case['address'])

        s = Center.query.filter_by(id=new_center.id).first()
        self.assertIsNot(s, None)
        self.assertEqual(s.login, test_case['login'])
        self.assertEqual(s.password, test_case['password'])
        self.assertEqual(s.address, test_case['address'])

    def test_field_type(self):
        test_case = {'login': 'true', 'password': 4, 'address' : 44}
        self.assertRaises(TypeError,
                          Center.add_center,
                          _login=test_case['login'],
                          _password=test_case['password'],
                          _address=test_case['address'])

    def test_valid_credentials(self):
        test_cases = [
            {'login': 'User1', 'password': 'pass1', 'address' : 'address 1', 'result': True},
            {'login': 'User2', 'password': 'pass2', 'address' : 'address 2', 'result': False}
        ]
        Center.add_center(test_cases[0]['login'], test_cases[0]['password'], test_cases[0]['address'])

        for test in test_cases:
            self.assertEqual(Center.valid_credentials(test['login'], test['password']), test['result'])



    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()