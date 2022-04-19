from flask import url_for

from company.models import Office
from tests.e2e.auth.fixtures import get_auth_headers


class TestOfficeCreate:

    def test_create_office(self, client, create_user, create_company, create_location):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        country, region, city = create_location()

        request_data = {
            'name': 'Office',
            'address': 'Address',
            'country_id': country.id,
            'region_id': region.id,
            'city_id': city.id,
        }

        response = client.post(
            url_for('company.office_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 201

        assert Office.query.filter_by(company_id=company.id).count() == 1

    def test_create_multiple_offices(self, client, create_user, create_company, create_location):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        country, region, city = create_location()

        request_data = {
            'name': 'Office',
            'address': 'Address',
            'country_id': country.id,
            'region_id': region.id,
            'city_id': city.id,
        }

        response = client.post(
            url_for('company.office_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 201

        response = client.post(
            url_for('company.office_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 201

        assert Office.query.filter_by(company_id=company.id).count() == 2

    def test_create_office_with_missed_fields(self, client, create_user, create_company, create_location):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        country, region, city = create_location()

        request_data = {
            'name': '',
            'address': 'Address',
            'country_id': country.id,
            'region_id': region.id,
            'city_id': city.id,
        }

        response = client.post(
            url_for('company.office_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 400

        request_data['name'] = None

        response = client.post(
            url_for('company.office_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 400

        del request_data['name']

        response = client.post(
            url_for('company.office_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 400

    def test_create_office_with_not_existing_location(self, client, create_user, create_company, create_location):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        country, region, city = create_location()

        request_data = {
            'name': 'Office',
            'address': 'Address',
            'country_id': 999,
            'region_id': region.id,
            'city_id': city.id,
        }

        response = client.post(
            url_for('company.office_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 400

    def test_create_office_with_unrelated_location(self, client, create_user, create_company, create_location,
                                                   create_country):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        country, region, city = create_location()
        country = create_country()

        request_data = {
            'name': 'Office',
            'address': 'Address',
            'country_id': country.id,
            'region_id': region.id,
            'city_id': city.id,
        }

        response = client.post(
            url_for('company.office_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 400

    def test_create_office_without_authentication(self, client, create_user, create_company, create_location):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        country, region, city = create_location()

        request_data = {
            'name': 'Office',
            'address': 'Address',
            'country_id': country.id,
            'region_id': region.id,
            'city_id': city.id,
        }

        response = client.post(
            url_for('company.office_create', company_id=company.id),
            json=request_data,
        )

        assert response.status_code == 401

    def test_create_office_with_not_existing_company(self, client, create_user, create_company, create_location):
        owner = create_user(email='owner@gmail.com')

        country, region, city = create_location()

        request_data = {
            'name': 'Office',
            'address': 'Address',
            'country_id': country.id,
            'region_id': region.id,
            'city_id': city.id,
        }

        response = client.post(
            url_for('company.office_create', company_id=999),
            json=request_data,
            headers=get_auth_headers(owner)
        )

        assert response.status_code == 404

    def test_create_office_by_employee(self, client, create_user, create_company, create_employee, create_location):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        user = create_user()
        employee = create_employee(user, company)

        country, region, city = create_location()

        request_data = {
            'name': 'Office',
            'address': 'Address',
            'country_id': country.id,
            'region_id': region.id,
            'city_id': city.id,
        }

        response = client.post(
            url_for('company.office_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(user),
        )

        assert response.status_code == 403
