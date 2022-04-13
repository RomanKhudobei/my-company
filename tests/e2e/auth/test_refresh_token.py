from flask import url_for
from flask_jwt_extended import create_refresh_token, decode_token

from tests.e2e.auth.fixtures import get_auth_headers


def test_refresh_token(client, create_user):
    user = create_user(
        first_name='test',
        last_name='test',
        email='test@gmail.com',
        password='testabc123',
    )

    refresh_token = create_refresh_token(user)

    response = client.post(url_for('auth.refresh-token'), headers=get_auth_headers(refresh_token))

    assert response.status_code == 200

    assert response.json.get('refresh_token') is None

    access_token = response.json.get('access_token')
    assert access_token

    access_token_payload = decode_token(access_token)
    assert access_token_payload.get('sub') == user.id


def test_refresh_token_without_token(client, create_user):
    response = client.post(url_for('auth.refresh-token'))
    assert response.status_code == 401
