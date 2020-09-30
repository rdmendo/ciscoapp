from datetime import datetime
from ciscoapp import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    def __repr__(self):
        return f"User: {self.username}"
    

class AdvertisedNetwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.String(16), nullable=False)
    task = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)


    def __repr__(self):
        return f"Network {self.prefix}-{self.task}-{self.date_posted}"
    
class Reroute(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ipaddress = db.Column(db.String(16), nullable=False)
    isp = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"Network {self.ipaddress}-{self.isp}-{self.date_posted}"