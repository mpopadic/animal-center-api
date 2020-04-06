from datetime import datetime


class AccessRequest:

    def __init__(self, center_id):
        self.center_id = center_id
        self.timestamp = datetime.now()


