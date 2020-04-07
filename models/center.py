import json

from database import db


class Center(db.Model):
    __tablename__ = "centers"

    id = db.Column('id', db.Integer, autoincrement=True, primary_key=True)
    _login = db.Column('login', db.String(30), nullable=False)
    _password = db.Column('password', db.String(50), nullable=False)
    _address = db.Column('address', db.String(50))
    animals = db.relationship("Animal", backref="owner")

    def __init__(self, login, password, address):
        self.login = login
        self.password = password
        self.address = address

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        if not isinstance(value, str):
            raise TypeError('login must be a string')
        self._login = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if not isinstance(value, str):
            raise TypeError('password must be a string')
        self._password = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if not isinstance(value, str):
            raise TypeError('address must be a string')
        self._address = value

    @staticmethod
    def json(center):
        return {'id': center.id, 'login': center.login, 'password': center.password,
                'address': center.address, 'animals': ["{0} - {1} - {2}".format(a.name, a.id, a.species) for a in center.animals]}

    @staticmethod
    def valid_credentials(_login, _password):
        center = Center.query.filter_by(_login=_login, _password=_password).first()
        print("CENTER: ", center)
        print("Type: ", type(center))
        if center:
            return True
        else:
            return False

    @staticmethod
    def get_all_centers():
        return ['{0} - {1}'.format(center.login, center.id) for center in Center.query.all()]

    @staticmethod
    def get_center_by_id(_id):
        center = Center.query.filter_by(id=_id).first()
        if center:
            return Center.json(center)
        else:
            return {}

    @staticmethod
    def add_center(_login, _password, _address):
        new_center = Center(_login, _password, _address)
        db.session.add(new_center)
        db.session.commit()

    @staticmethod
    def is_valid_object(center):
        return center.get('login', None) is not None \
               and center.get('password', None) is not None \
               and center.get('address', None) is not None

    def __repr__(self):
        center_object = {
            'login': self.login,
            'password': self.password,
            'address': self.password
        }
        return json.dumps(center_object)


