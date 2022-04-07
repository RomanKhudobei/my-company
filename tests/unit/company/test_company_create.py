from flask import url_for

from tests.unit.auth.fixtures import get_auth_headers


def test_company_create(client, create_user):
    user = create_user(
        first_name='test',
        last_name='test',
        email='test@gmail.com',
        password='testabc123',
    )
    request_data = {
        'company_name': 'Test',
    }
    response = client.post(url_for('company.create'), json=request_data, headers=get_auth_headers(user))

    assert response.status_code == 201

    company = response.json.get('company')

    assert company

    assert company.get('id')
    assert company.get('name') == 'Test'
    assert company.get('address') is None
    assert company.get('owner') == user.id


def test_company_create_without_authentication(client, create_user):
    request_data = {
        'company_name': 'Test',
    }
    response = client.post(url_for('company.create'), json=request_data)
    assert response.status_code == 401
