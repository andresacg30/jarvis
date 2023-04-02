from app import db
from app.models import User


def create_guest_user() -> int:
    user = User(is_guest=True)
    db.session.add(user)
    db.session.commit()

    return user
