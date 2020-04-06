from database import db

class Center(db.Model):
    __tablename__ = "centers"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50))

    def __init__(self, login, password, address):

        self.login = login
        self.password = password
        self.address = address


