import typing

from app import db
from app.models import Lead
from app.utils import constants


def create_lead(
    name: str,
    email: str,
    phone_number: str,
    birthday: str,
    have_iul: bool,
    primary_goal: str,
    state: str,
    campaign: str
) -> Lead:
    lead = Lead(
        name=name,
        email=email,
        phone_number=phone_number,
        birthday=birthday,
        have_iul=have_iul,
        primary_goal=primary_goal,
        state=state,
        campaign=campaign
    )
    db.session.add(lead)
    db.session.commit()

    return lead


def get_lead_by_phone_number(phone_number: str) -> typing.Optional[Lead]:
    return Lead.query.filter_by(phone_number=phone_number).first()


def get_lead_setup(lead: Lead) -> str:
    return constants.LEAD_SETUP.format(lead.name, lead.campaign, lead.primary_goal)


def get_lead_by_email(email: str) -> typing.Optional[Lead]:
    return Lead.query.filter_by(email=email).first()
