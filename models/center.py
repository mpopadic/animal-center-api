import uuid


class Center:

    def __init__(self, login, password, address):
        self.id = uuid.uuid4()
        self.login = login
        self.password = password
        self.address = address


