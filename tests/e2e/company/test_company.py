from flask import url_for

from app.db import db
from company.models import Company
from tests.e2e.auth.fixtures import get_auth_headers


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

    def test_company_create_twice(self, client, create_user):
        user = create_user()
        request_data = {
            'name': 'Test',
        }

        response = client.post(url_for('company.create'), json=request_data, headers=get_auth_headers(user))
        assert response.status_code == 201

        response = client.post(url_for('company.create'), json=request_data, headers=get_auth_headers(user))
        assert response.status_code == 400

    def test_company_create_without_authentication(self, client, create_user):
        request_data = {
            'name': 'Test',
        }
        response = client.post(url_for('company.create'), json=request_data)
        assert response.status_code == 401

    def test_create_company_by_employee(self, client, create_user, create_company, create_employee):
        user = create_user()

        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        create_employee(user, company)

        request_data = {
            'name': 'Test',
        }
        response = client.post(url_for('company.create'), json=request_data, headers=get_auth_headers(user))

        assert response.status_code == 400

        assert Company.query.filter_by(owner=user).one_or_none() is None


class TestCompanyRetrieve:

    def test_company_retrieve(self, client, create_user, create_company):
        user = create_user()
        company = create_company(user)

        response = client.get(url_for('company.retrieve', company_id=company.id), headers=get_auth_headers(user))

        assert response.status_code == 200
        assert response.json.get('id') == company.id

    def test_company_retrieve_not_by_owner(self, client, create_user, create_company):
        user = create_user()
        company = create_company(user)

        another_user = create_user(email='test@gmail.com')
        response = client.get(
            url_for('company.retrieve', company_id=company.id),
            headers=get_auth_headers(another_user)
        )

        assert response.status_code == 404

    def test_company_retrieve_without_authentication(self, client, create_user, create_company):
        user = create_user()
        company = create_company(user)

        response = client.get(url_for('company.retrieve', company_id=company.id))

        assert response.status_code == 401

    def test_company_retrieve_not_exist(self, client, create_user, create_company):
        user = create_user()
        response = client.get(url_for('company.retrieve', company_id=999), headers=get_auth_headers(user))
        assert response.status_code == 404


class TestCompanyUpdate:

    def test_company_update(self, client, create_user, create_company):
        user = create_user()
        company = create_company(user)

        request_data = {
            'name': 'Updated test',
            'address': 'Updated address',
        }
        response = client.put(
            url_for('company.update', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(user)
        )

        assert response.status_code == 200

        db.session.refresh(company)

        assert company.name == request_data.get('name') == response.json.get('name')
        assert company.address == request_data.get('address') == response.json.get('address')

    def test_company_update_company_id(self, client, create_user, create_company):
        user = create_user()
        company = create_company(user)
        company_id = company.id

        request_data = {
            'id': 999,
            'name': 'Updated test',
            'address': 'Updated address',
        }
        response = client.put(
            url_for('company.update', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(user)
        )

        assert response.status_code == 400

        db.session.refresh(company)

        assert company.id == company_id

    def test_company_update_owner_id(self, client, create_user, create_company):
        user = create_user()
        company = create_company(user)

        request_data = {
            'owner_id': 999,
            'name': 'Updated test',
            'address': 'Updated address',
        }
        response = client.put(
            url_for('company.update', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(user)
        )

        assert response.status_code == 400

    def test_company_update_by_another_user(self, client, create_user, create_company):
        user = create_user()
        company_data = {
            'name': 'Test',
            'address': 'Test',
        }
        company = create_company(user, **company_data)

        request_data = {
            'name': 'Updated test',
            'address': 'Updated address',
        }
        another_user = create_user(email='test@gmail.com')
        response = client.put(
            url_for('company.update', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(another_user)
        )

        assert response.status_code == 404

        db.session.refresh(company)

        assert company.name == company_data.get('name')
        assert company.address == company_data.get('address')

    def test_company_update_not_exist(self, client, create_user, create_company):
        user = create_user()

        request_data = {
            'name': 'Updated test',
            'address': 'Updated address',
        }
        response = client.put(
            url_for('company.update', company_id=999),
            json=request_data,
            headers=get_auth_headers(user)
        )

        assert response.status_code == 404

    def test_company_update_with_empty_name(self, client, create_user, create_company):
        user = create_user()
        company_data = {
            'name': 'Test',
            'address': 'Test',
        }
        company = create_company(user, **company_data)

        request_data = {
            'name': '',
            'address': 'Updated address',
        }
        response = client.put(
            url_for('company.update', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(user)
        )

        assert response.status_code == 400

        db.session.refresh(company)

        assert company.name == company_data.get('name')
        assert company.address == company_data.get('address')

        request_data = {
            'name': None,
            'address': 'Updated address',
        }
        response = client.put(
            url_for('company.update', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(user)
        )

        assert response.status_code == 400

        del request_data['name']
        response = client.put(
            url_for('company.update', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(user)
        )

        assert response.status_code == 400

    def test_company_update_with_unknown_field(self, client, create_user, create_company):
        user = create_user()
        company_data = {
            'name': 'Test',
            'address': 'Test',
        }
        company = create_company(user, **company_data)

        request_data = {
            'name': 'Updated name',
            'address': 'Updated address',
            'unknown': 'field'
        }
        response = client.put(
            url_for('company.update', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(user)
        )

        assert response.status_code == 400

        db.session.refresh(company)

        assert company.name == company_data.get('name')
        assert company.address == company_data.get('address')
