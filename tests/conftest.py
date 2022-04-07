import pytest

from app.db import db
from app.factory import create_app
from user.models import User


@pytest.fixture
def app():
    test_db_url = 'postgresql://test:test@db_test:5432/test'
    app = create_app(test_config={
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': test_db_url,
        'DATABASE_URL': test_db_url,
        'SECRET_KEY': 'test-secret',
    })
    app_context = app.app_context()
    app_context.push()

    db.drop_all()
    db.create_all()

    yield app

    db.session.remove()
    db.drop_all()


@pytest.fixture(autouse=True)
def clear_db():
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(f'TRUNCATE "{table.name}" RESTART IDENTITY CASCADE;')


@pytest.fixture
def create_user():

    def make_create_user(**kwargs):
        user = User(**kwargs)
        db.session.add(user)
        db.session.commit()
        return user

    return make_create_user
