import json

from database import db


class Center(db.Model):
    """This class represent centers table. Used to store Center objects in DB."""

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
        """Converts given Center object to json formatted data"""
        return {'id': center.id, 'login': center.login, 'password': center.password,
                'address': center.address, 'animals': ["{0} - {1} - {2}".format(a.name, a.id, a.species) for a in center.animals]}

    @staticmethod
    def valid_credentials(_login, _password):
        """Checks if login and password are valid and returns boolean."""
        center = Center.query.filter_by(_login=_login, _password=_password).first()
        if center:
            return True
        else:
            return False

    @staticmethod
    def get_all_centers():
        """Fetches all centers from DB."""
        return ['{0} - {1}'.format(center.login, center.id) for center in Center.query.all()]

    @staticmethod
    def get_center_by_id(_id):
        """Fetches center from DB with given id. If doesn't exists returns empty dict."""
        center = Center.query.filter_by(id=_id).first()
        if center:
            return Center.json(center)
        else:
            return {}

    @staticmethod
    def add_center(_login, _password, _address):
        """Creates new Center in DB."""
        new_center = Center(_login, _password, _address)
        db.session.add(new_center)
        db.session.commit()
        return new_center

    @staticmethod
    def is_valid_object(center):
        """Checks if given object have all required properties for creating Center object"""
        return 'login' in center and 'password' in center and 'address' in center

    def __repr__(self):
        center_object = {
            'login': self.login,
            'password': self.password,
            'address': self.password
        }
        return json.dumps(center_object)


