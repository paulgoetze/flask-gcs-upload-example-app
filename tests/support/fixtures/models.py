import pytest
from sqlalchemy.orm import Session

from my_app import db
from my_app.users.models import User


@pytest.fixture
def user(session: Session) -> db.Model:
    user = User(email='user@example.com')
    session.add(user)
    session.commit()

    return user


