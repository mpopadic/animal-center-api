import json

from database import db


class Center(db.Model):
    __tablename__ = "centers"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    login = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50))

    def __init__(self, login, password, address):
        self.login = login
        self.password = password
        self.address = address

    @staticmethod
    def json(center):
        return {'id': center.id, 'login': center.login, 'password': center.password, 'address': center.address}

    @staticmethod
    def valid_credentials(_login, _password):
        center = Center.query.filter_by(login=_login, password=_password).first()
        if center:
            return True
        else:
            return False

    @staticmethod
    def get_all_centers():
        return [Center.json(center) for center in Center.query.all()]

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
        return center.login is None or center.password is None or center.address is None

    def __repr__(self):
        center_object = {
            'login': self.login,
            'password': self.password,
            'address': self.password
        }
        return json.dumps(center_object)


