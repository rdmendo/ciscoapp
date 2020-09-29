from datetime import datetime
from ciscoapp import db


class AdvertisedNetwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.String(16), nullable=False)
    task = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)


    def __repr__(self):
        return f"Network {self.prefix}-{self.task}-{self.date_posted}"
