from datetime import datetime
from ciscoapp import db


class Dhcp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ipaddress = db.Column(db.String(20), unique=True, nullable=False)
    pool = db.Column(db.String(120), unique=True, nullable=False)
    # private_ip = db.Column(db.String(120), unique=True, nullable=False)
    # interface = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Dhcp {self.ipaddress}, {self.pool}"
