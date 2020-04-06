from datetime import datetime
from database import db

class AccessRequest(db.Model):
    __tablename__ = "access_requests"

    id = db.Column(db.Integer, primary_key=True)
    center_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.TIMESTAMP)

    def __init__(self, center_id):
        self.center_id = center_id
        self.timestamp = datetime.now()


