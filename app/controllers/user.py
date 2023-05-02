import typing

from app import db
from app.models import User


def create_guest_user() -> int:
    user = User(is_guest=True)
    db.session.add(user)
    db.session.commit()

    return user


def create_user(name: str, phone_number: str, origin: str) -> int:
    user = User(
        name=name,
        is_guest=False,
        phone_number=phone_number,
        origin=origin
    )
    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_phone_number(phone_number: str) -> typing.Optional[User]:
    return User.query.filter_by(phone_number=phone_number).first()
