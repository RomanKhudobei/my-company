import pytest
from flask import url_for
from marshmallow import ValidationError

from tests.unit.user.fixtures import get_user_data
from user.models import User
from user.schemas import UserSchema


def test_create_user(client):
    request_data = get_user_data()
    response = client.post(url_for('user.create'), json=request_data)

    assert response.status_code == 201

    # check all fields returned
    try:
        UserSchema().load(response.json)
    except ValidationError as e:
        pytest.fail(str(e))

    user = User.query.filter_by(email=response.json['email']).first()
    assert user


def test_create_user_with_already_exist_email(client):
    request_data = get_user_data()
    response = client.post(url_for('user.create'), json=request_data)

    assert response.status_code == 201

    response = client.post(url_for('user.create'), json=request_data)

    assert response.status_code == 400
    assert response.json.get('email')   # error message

    assert User.query.filter_by(email=request_data['email']).count() == 1


def test_create_user_with_invalid_email(client):
    request_data = get_user_data()
    request_data['email'] = 'not_valid_email'
    response = client.post(url_for('user.create'), json=request_data)

    assert response.status_code == 400

    assert response.json.get('email')   # error message


def test_create_user_with_missed_fields(client):
    data = get_user_data()
    data.pop('password')
    data.pop('repeat_password')

    fields = list(data.keys())

    for field in fields:
        request_data = get_user_data()

        request_data[field] = ''
        response = client.post(url_for('user.create'), json=request_data)
        assert response.status_code == 400
        assert response.json.get(field)

        request_data[field] = None
        response = client.post(url_for('user.create'), json=request_data)
        assert response.status_code == 400
        assert response.json.get(field)

        del request_data[field]
        response = client.post(url_for('user.create'), json=request_data)
        assert response.status_code == 400
        assert response.json.get(field)

        assert User.query.count() == 0


def test_create_user_with_missed_password_fields(client):
    request_data = get_user_data()

    request_data['password'] = ''
    request_data['repeat_password'] = ''
    response = client.post(url_for('user.create'), json=request_data)
    assert response.status_code == 400
    assert response.json.get('password')
    assert response.json.get('repeat_password')

    request_data['password'] = None
    request_data['repeat_password'] = None
    response = client.post(url_for('user.create'), json=request_data)
    assert response.status_code == 400
    assert response.json.get('password')
    assert response.json.get('repeat_password')

    del request_data['password']
    del request_data['repeat_password']
    response = client.post(url_for('user.create'), json=request_data)
    assert response.status_code == 400
    assert response.json.get('password')
    assert response.json.get('repeat_password')

    assert User.query.count() == 0
