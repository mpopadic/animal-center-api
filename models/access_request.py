from datetime import datetime
from database import db

class AccessRequest(db.Model):
    __tablename__ = "access_requests"

    id = db.Column(db.Integer, primary_key=True)
    center_id = db.Column(db.Integer, db.ForeignKey("centers.id"))
    timestamp = db.Column(db.TIMESTAMP)

    def __init__(self, center_id):
        self.center_id = center_id
        self.timestamp = datetime.now()

    @staticmethod
    def json(ac):
        return {'id': ac.id, 'center_id': ac.center_id, 'timestamp': ac.timestamp}

    @staticmethod
    def get_all_access_requests():
        return [AccessRequest.json(ac) for ac in AccessRequest.query.all()]

    @staticmethod
    def add_access_request(_center_id):
        new_access_request = AccessRequest(_center_id)
        db.session.add(new_access_request)
        db.session.commit()