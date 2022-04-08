from flask import url_for

from app.db import db
from tests.unit.auth.fixtures import get_auth_headers
from tests.unit.user.fixtures import get_user_data
from user.models import User


class TestUserCreate:

    def test_create_user(self, client):
        request_data = get_user_data()
        response = client.post(url_for('user.create'), json=request_data)

        assert response.status_code == 201

        user = User.query.filter_by(email=response.json['email']).first()
        assert user

    def test_create_user_with_already_exist_email(self, client):
        request_data = get_user_data()
        response = client.post(url_for('user.create'), json=request_data)

        assert response.status_code == 201

        response = client.post(url_for('user.create'), json=request_data)

        assert response.status_code == 400
        assert response.json.get('email')   # error message

        assert User.query.filter_by(email=request_data['email']).count() == 1

    def test_create_user_with_invalid_email(self, client):
        request_data = get_user_data()
        request_data['email'] = 'not_valid_email'
        response = client.post(url_for('user.create'), json=request_data)

        assert response.status_code == 400

        assert response.json.get('email')   # error message

    def test_create_user_with_missed_fields(self, client):
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

    def test_create_user_with_missed_password_fields(self, client):
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


class TestUserRetrieve:

    def test_user_retrieve(self, client, create_user):
        user = create_user()

        response = client.get(url_for('user.retrieve', user_id=user.id), headers=get_auth_headers(user))

        assert response.status_code == 200
        assert response.json.get('id') == user.id

    def test_user_retrieve_by_another_user(self, client, create_user):
        user = create_user()

        another_user = create_user(email='test@gmail.com')
        response = client.get(url_for('user.retrieve', user_id=user.id), headers=get_auth_headers(another_user))

        assert response.status_code == 403

    def test_user_retrieve_without_authentication(self, client, create_user):
        user = create_user()
        response = client.get(url_for('user.retrieve', user_id=user.id))
        assert response.status_code == 401
