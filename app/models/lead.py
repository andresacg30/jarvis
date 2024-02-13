from app import db


class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone_number = db.Column(db.String(20), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    have_iul = db.Column(db.Boolean, nullable=True)
    primary_goal = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    campaign = db.Column(db.String(20), nullable=True)
