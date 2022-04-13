from flask import url_for
from flask_jwt_extended import decode_token


def test_user_login(client, create_user):
    email = 'test@gmail.com'
    password = 'testabc123'
    user = create_user(
        email=email,
        password=password,
    )

    request_data = {
        'email': email,
        'password': password,
    }
    response = client.post(url_for('auth.login'), json=request_data)

    assert response.status_code == 200

    access_token = response.json.get('access_token')
    refresh_token = response.json.get('refresh_token')

    assert access_token
    assert refresh_token

    access_token_payload = decode_token(access_token)
    refresh_token_payload = decode_token(access_token)

    assert access_token_payload.get('sub') == user.id
    assert refresh_token_payload.get('sub') == user.id


def test_user_login_with_invalid_credentials(client, create_user):
    email = 'test@gmail.com'
    password = 'testabc123'
    create_user(
        email=email,
        password=password,
    )

    request_data = {
        'email': email,
        'password': 'invalid',
    }
    response = client.post(url_for('auth.login'), json=request_data)

    assert response.status_code == 401


def test_not_existing_user_login(client, create_user):
    request_data = {
        'email': 'test@gmail.com',
        'password': 'invalid',
    }
    response = client.post(url_for('auth.login'), json=request_data)

    assert response.status_code == 401
