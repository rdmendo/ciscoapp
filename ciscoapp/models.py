from datetime import datetime
from ciscoapp import db


class AdvertisedNetwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.String(16), unique=True, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __repr__(self):
        return f"Network {self.prefix}, {self.date_posted}"
