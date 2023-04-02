import pytest
from app.models import Conversation


@pytest.fixture
def conversation_factory(db_session):

    def create_conversation(user_id):
        conversation = Conversation(user_id=user_id)
        try:
            db_session.add(conversation)
            db_session.commit()
        finally:
            db_session.rollback()
        return conversation

    return create_conversation
