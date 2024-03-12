import datetime
import typing

from app import db
from app.models import Lead
from app.utils import constants

import app.controllers.message as message_controller
from app.models import Message


class LeadNotFoundError(Exception):
    """
    Raised if lead is not found.
    """


def create_lead(
    name: str,
    email: str,
    phone_number: str,
    birthday: str,
    have_iul: bool,
    primary_goal: str,
    state: str,
    campaign: str,
    lead_type: str
) -> Lead:
    try:
        date = datetime.datetime.strptime(birthday, "%Y-%m-%d") if birthday != "null" else None
    except ValueError:
        date = None
    lead = Lead(
        name=name,
        email=email,
        phone_number=phone_number,
        birthday=date,
        have_iul=have_iul,
        primary_goal=primary_goal,
        state=state,
        campaign=campaign,
        lead_type=lead_type
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


def get_lead_by_name(name: str) -> typing.Optional[Lead]:
    return Lead.query.filter_by(name=name).first()


def find_lead_by_message(message: str) -> typing.Optional[Lead]:
    prompt = f"Extract the name from this message: {message}. Only return the name without quotation marks."
    messages = [
        Message(role="system", content=prompt)
    ]
    find_lead = message_controller.get_model_response(messages=messages)
    lead = get_lead_by_name(find_lead)
    if not lead:
        raise LeadNotFoundError(f"Lead with name {find_lead} not found")
    return lead
