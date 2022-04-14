import pytest

from app.db import db
from app.factory import create_app
from company.models import Company, Employee
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

    def make_create_user(first_name='John', last_name='Doe', email='john.doe@gmail.com', password='test', **kwargs):
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            **kwargs
        )
        db.session.add(user)
        db.session.commit()
        return user

    return make_create_user


@pytest.fixture
def create_company():

    def make_create_company(user, name='Test', **kwargs):
        company = Company(owner=user, name=name, **kwargs)
        db.session.add(company)
        db.session.commit()
        return company

    return make_create_company


@pytest.fixture
def create_employee():

    def make_create_employee(user, company):
        employee = Employee(user=user, company=company)
        db.session.add(employee)
        db.session.commit()
        return employee

    return make_create_employee
