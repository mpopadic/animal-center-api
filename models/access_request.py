from datetime import datetime
from database import db


class AccessRequest(db.Model):
    """Class that represent access_request table in DB. Used to store information when someone requires a token."""

    __tablename__ = "access_requests"

    id = db.Column(db.Integer, primary_key=True)
    _center_id = db.Column('center_id', db.Integer, db.ForeignKey("centers.id"))
    timestamp = db.Column(db.TIMESTAMP)

    def __init__(self, center_id):
        self.center_id = center_id
        self.timestamp = datetime.now()

    @property
    def center_id(self):
        return self._center_id

    @center_id.setter
    def center_id(self, value):
        if not isinstance(value, int) or type(value) is not int:
            raise TypeError('center_id must be a int')
        self._center_id = value

    @staticmethod
    def json(ac):
        """Converts given AccessRequest object to json formatted data"""
        return {'id': ac.id, 'center_id': ac.center_id, 'timestamp': ac.timestamp}

    @staticmethod
    def get_all_access_requests():
        """Get all rows from table access_request"""
        return [AccessRequest.json(ac) for ac in AccessRequest.query.all()]

    @staticmethod
    def add_access_request(_center_id):
        """Adds new access request to DB"""
        new_access_request = AccessRequest(_center_id)
        db.session.add(new_access_request)
        db.session.commit()