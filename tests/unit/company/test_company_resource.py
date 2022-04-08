import pytest
from flask import url_for
from marshmallow import ValidationError

from company.models import Company
from company.schemas import CompanySchema
from tests.unit.auth.fixtures import get_auth_headers


class TestCompanyCreate:

    def test_company_create(self, client, create_user):
        user = create_user()
        request_data = {
            'name': 'Test',
        }
        response = client.post(url_for('company.create'), json=request_data, headers=get_auth_headers(user))

        assert response.status_code == 201

        company = response.json

        assert company

        assert company.get('id')
        assert company.get('name') == 'Test'
        assert company.get('address') is None

        assert Company.query.filter_by(owner=user).one_or_none()

    def test_company_create_without_authentication(self, client, create_user):
        request_data = {
            'name': 'Test',
        }
        response = client.post(url_for('company.create'), json=request_data)
        assert response.status_code == 401


class TestCompanyRetrieve:

    def test_company_retrieve(self, client, create_user, create_company):
        user = create_user()
        company = create_company(user)

        response = client.get(url_for('company.retrieve', company_id=company.id), headers=get_auth_headers(user))

        assert response.status_code == 200
        assert response.json.get('id') == company.id

        try:
            CompanySchema().load(response.json)
        except ValidationError as e:
            pytest.fail(str(e))

    def test_company_retrieve_not_by_owner(self, client, create_user, create_company):
        user = create_user()
        company = create_company(user)

        another_user = create_user(email='test@gmail.com')
        response = client.get(
            url_for('company.retrieve', company_id=company.id),
            headers=get_auth_headers(another_user)
        )

        assert response.status_code == 403

    def test_company_retrieve_without_authentication(self, client, create_user, create_company):
        user = create_user()
        company = create_company(user)

        response = client.get(url_for('company.retrieve', company_id=company.id))

        assert response.status_code == 401

    def test_company_retrieve_not_exist(self, client, create_user, create_company):
        user = create_user()
        response = client.get(url_for('company.retrieve', company_id=999), headers=get_auth_headers(user))
        assert response.status_code == 404
