from datetime import datetime

from app import db
from .message import Message


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'))
    messages = db.relationship("Message", lazy='dynamic')
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_finished = db.Column(db.Boolean, nullable=False, default=False)

    def add_message(self, role, content):
        message = Message(role=role, content=content, conversation_id=self.id)
        db.session.add(message)
        self.messages.append(message)
        db.session.commit()
        return message
