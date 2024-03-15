from app import db


class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone_number = db.Column(db.String(20), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    have_iul = db.Column(db.Boolean, nullable=True)
    primary_goal = db.Column(db.String(300), nullable=True)
    state = db.Column(db.String(20), nullable=True)
    campaign = db.Column(db.String(20), nullable=True)
    lead_type = db.Column(db.String(20), nullable=True)
    other_fields = db.Column(db.JSON, nullable=True)
