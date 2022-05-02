import pytest
from flask import url_for

from app.db import db
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

    def test_create_office_with_missed_location_fields(self, client, create_user, create_company, create_location):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        country, region, city = create_location()

        request_data = {
            'name': 'Name',
            'address': 'Address',
            'country_id': '',
            'region_id': region.id,
            'city_id': city.id,
        }

        response = client.post(
            url_for('company.office_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 400

        request_data['country_id'] = None

        response = client.post(
            url_for('company.office_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 400

        del request_data['country_id']

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


class TestOfficeList:

    def test_list_offices(self, client, create_user, create_company, create_office):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        for _ in range(5):
            create_office(company)

        owner2 = create_user(email='owner2@gmail.com')
        company2 = create_company(owner2)

        for _ in range(5):
            create_office(company2)

        response = client.get(url_for('company.office_list', company_id=company.id), headers=get_auth_headers(owner))

        assert response.status_code == 200

        assert len(response.json) == 5

    @pytest.mark.parametrize(
        'query,result_count',
        [
            ('', 16),
            ('?test=1', 16),
            ('?country_id=1', 8),
            ('?region_id=1', 4),
            ('?city_id=1', 2),
            ('?country_id=999', 0),
            ('?country_id=1&region_id=1', 4),
            ('?country_id=1&region_id=2', 0),
        ]
    )
    def test_office_list_search_by_location(self, client, create_user, create_company, create_office, query,
                                            result_count, create_country, create_region, create_city):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        countries = [create_country(name='C1'), create_country(name='C2')]

        regions = []
        for i in range(4):
            regions.append(create_region(countries[i % 2], name=f'R{i}'))

        cities = []
        for i in range(8):
            cities.append(create_city(countries[i % 2], regions[i % 4], name=f'C{i}'))

        for i in range(16):
            create_office(company, country=countries[i % 2], region=regions[i % 4], city=cities[i % 8])

        response = client.get(
            url_for('company.office_list', company_id=company.id) + query,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 200

        assert len(response.json) == result_count

    def test_list_offices_without_authentication(self, client, create_user, create_company, create_office):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        for _ in range(5):
            create_office(company)

        response = client.get(url_for('company.office_list', company_id=company.id))

        assert response.status_code == 401

    def test_list_offices_by_employee(self, client, create_user, create_company, create_office, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        for _ in range(5):
            create_office(company)

        user = create_user()
        create_employee(user, company)
        response = client.get(url_for('company.office_list', company_id=company.id), headers=get_auth_headers(user))

        assert response.status_code == 200

        assert len(response.json) == 5

    def test_list_offices_not_by_owner_or_employee(self, client, create_user, create_company, create_office):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        for _ in range(5):
            create_office(company)

        user = create_user()
        response = client.get(url_for('company.office_list', company_id=company.id), headers=get_auth_headers(user))

        assert response.status_code == 403


class TestOfficeRetrieve:

    def test_retrieve_office(self, client, create_user, create_company, create_office):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        response = client.get(
            url_for('company.office_retrieve', company_id=company.id, office_id=office.id),
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 200
        assert response.json.get('id') == office.id

    def test_retrieve_office_without_authentication(self, client, create_user, create_company, create_office):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        response = client.get(
            url_for('company.office_retrieve', company_id=company.id, office_id=office.id),
        )

        assert response.status_code == 401

    def test_retrieve_office_not_by_owner(self, client, create_user, create_company, create_office):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        response = client.get(
            url_for('company.office_retrieve', company_id=company.id, office_id=office.id),
            headers=get_auth_headers(create_user()),
        )

        assert response.status_code == 403

    def test_retrieve_office_by_owner_of_another_company(self, client, create_user, create_company, create_office):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        another_owner = create_user(email='another_owner@gmail.com')
        another_company = create_company(another_owner)
        response = client.get(
            url_for('company.office_retrieve', company_id=company.id, office_id=office.id),
            headers=get_auth_headers(another_owner),
        )

        assert response.status_code == 403

    def test_retrieve_office_by_employee(self, client, create_user, create_company, create_office, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company)

        response = client.get(
            url_for('company.office_retrieve', company_id=company.id, office_id=office.id),
            headers=get_auth_headers(user),
        )

        assert response.status_code == 403

    def test_retrieve_not_existing_office(self, client, create_user, create_company, create_office):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        response = client.get(
            url_for('company.office_retrieve', company_id=company.id, office_id=999),
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 404

    def test_retrieve_office_from_not_existing_company(self, client, create_user, create_company, create_office):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        response = client.get(
            url_for('company.office_retrieve', company_id=999, office_id=999),
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 404


class TestOfficeUpdate:

    def test_update_office(self, client, create_user, create_company, create_office, create_location):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        office = create_office(company)

        country, region, city = create_location()
        request_data = {
            'name': 'Updated name',
            'address': 'Updated address',
            'country_id': country.id,
            'region_id': region.id,
            'city_id': city.id,
        }

        response = client.put(
            url_for('company.office_update', company_id=company.id, office_id=office.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 200

        db.session.refresh(office)

        assert response.json.get('name') == 'Updated name' == office.name
        assert response.json.get('address') == 'Updated address' == office.address
        assert response.json.get('country', {}).get('id') == country.id == office.country_id
        assert response.json.get('region', {}).get('id') == region.id == office.region_id
        assert response.json.get('city', {}).get('id') == city.id == office.city_id

    def test_update_office_with_missing_fields(self, client, create_user, create_company, create_office, create_location):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        office = create_office(company)

        country, region, city = create_location()
        request_data = {
            'name': 'Updated name',
            'address': 'Updated address',
            'country_id': country.id,
            'region_id': region.id,
            'city_id': city.id,
        }

        for field in request_data:
            data = request_data.copy()

            data[field] = None
            response = client.put(
                url_for('company.office_update', company_id=company.id, office_id=office.id),
                json=data,
                headers=get_auth_headers(owner),
            )
            assert response.status_code == 400

            data[field] = ''
            response = client.put(
                url_for('company.office_update', company_id=company.id, office_id=office.id),
                json=data,
                headers=get_auth_headers(owner),
            )
            assert response.status_code == 400

            del data[field]
            response = client.put(
                url_for('company.office_update', company_id=company.id, office_id=office.id),
                json=data,
                headers=get_auth_headers(owner),
            )
            assert response.status_code == 400

    def test_update_office_without_authentication(self, client, create_user, create_company, create_office, create_location):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        office = create_office(company)

        country, region, city = create_location()
        request_data = {
            'name': 'Updated name',
            'address': 'Updated address',
            'country_id': country.id,
            'region_id': region.id,
            'city_id': city.id,
        }

        response = client.put(
            url_for('company.office_update', company_id=company.id, office_id=office.id),
            json=request_data,
        )

        assert response.status_code == 401

    def test_update_office_by_employee(self, client, create_user, create_company, create_office, create_location,
                                       create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        office = create_office(company)

        user = create_user()
        create_employee(user, company)

        country, region, city = create_location()
        request_data = {
            'name': 'Updated name',
            'address': 'Updated address',
            'country_id': country.id,
            'region_id': region.id,
            'city_id': city.id,
        }

        response = client.put(
            url_for('company.office_update', company_id=company.id, office_id=office.id),
            json=request_data,
            headers=get_auth_headers(user),
        )

        assert response.status_code == 403

    def test_update_office_by_another_owner(self, client, create_user, create_company, create_office, create_location):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        office = create_office(company)

        another_owner = create_user(email='another_owner@gmail.com')
        another_company = create_company(another_owner)

        country, region, city = create_location()
        request_data = {
            'name': 'Updated name',
            'address': 'Updated address',
            'country_id': country.id,
            'region_id': region.id,
            'city_id': city.id,
        }

        response = client.put(
            url_for('company.office_update', company_id=company.id, office_id=office.id),
            json=request_data,
            headers=get_auth_headers(another_owner),
        )

        assert response.status_code == 403

    def test_update_office_by_another_user(self, client, create_user, create_company, create_office, create_location):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        office = create_office(company)

        user = create_user()

        country, region, city = create_location()
        request_data = {
            'name': 'Updated name',
            'address': 'Updated address',
            'country_id': country.id,
            'region_id': region.id,
            'city_id': city.id,
        }

        response = client.put(
            url_for('company.office_update', company_id=company.id, office_id=office.id),
            json=request_data,
            headers=get_auth_headers(user),
        )

        assert response.status_code == 403

    def test_update_office_company(self, client, create_user, create_company, create_office, create_location):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        office = create_office(company)

        country, region, city = create_location()
        request_data = {
            'company_id': 999,
            'name': 'Updated name',
            'address': 'Updated address',
            'country_id': country.id,
            'region_id': region.id,
            'city_id': city.id,
        }

        response = client.put(
            url_for('company.office_update', company_id=company.id, office_id=office.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 400

    def test_update_office_id(self, client, create_user, create_company, create_office, create_location):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        office = create_office(company)

        country, region, city = create_location()
        request_data = {
            'id': 999,
            'name': 'Updated name',
            'address': 'Updated address',
            'country_id': country.id,
            'region_id': region.id,
            'city_id': city.id,
        }

        response = client.put(
            url_for('company.office_update', company_id=company.id, office_id=office.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 400

    def test_update_someone_else_office(self, db, client, create_user, create_company, create_office, create_location):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        another_owner = create_user(email='another_owner@gmail.com')
        another_company = create_company(another_owner)
        another_company_office = create_office(another_company)

        country, region, city = create_location()
        request_data = {
            'name': 'Updated name',
            'address': 'Updated address',
            'country_id': country.id,
            'region_id': region.id,
            'city_id': city.id,
        }

        response = client.put(
            url_for('company.office_update', company_id=company.id, office_id=another_company_office.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 403


class TestOfficeDelete:

    def test_delete_office(self, client, create_user, create_company, create_office):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        office = create_office(company)

        response = client.delete(
            url_for('company.office_delete', company_id=company.id, office_id=office.id),
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 200

        assert Office.query.count() == 0

    def test_delete_office_without_authentication(self, client, create_user, create_company, create_office):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        office = create_office(company)

        response = client.delete(
            url_for('company.office_delete', company_id=company.id, office_id=office.id),
        )

        assert response.status_code == 401

    def test_delete_office_by_employee(self, client, create_user, create_company, create_office, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        user = create_user()
        create_employee(user, company)
        office = create_office(company)

        response = client.delete(
            url_for('company.office_delete', company_id=company.id, office_id=office.id),
            headers=get_auth_headers(user),
        )

        assert response.status_code == 403

    def test_delete_office_by_owner_of_another_business(self, client, create_user, create_company, create_office):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        office = create_office(company)

        another_owner = create_user(email='another_owner@gmail.com')
        another_company = create_company(another_owner)

        response = client.delete(
            url_for('company.office_delete', company_id=company.id, office_id=office.id),
            headers=get_auth_headers(another_owner),
        )

        assert response.status_code == 403

    def test_delete_someone_else_office(self, client, create_user, create_company, create_office):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        another_owner = create_user(email='another_owner@gmail.com')
        another_company = create_company(another_owner)
        another_office = create_office(another_company)

        response = client.delete(
            url_for('company.office_delete', company_id=company.id, office_id=another_office.id),
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 403

    def test_delete_not_existing_office(self, client, create_user, create_company):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        response = client.delete(
            url_for('company.office_delete', company_id=company.id, office_id=999),
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 404

    def test_delete_office_of_non_existing_company(self, client, create_user, create_company, create_office):
        owner = create_user(email='owner@gmail.com')

        response = client.delete(
            url_for('company.office_delete', company_id=999, office_id=999),
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 404


class TestAssignEmployeeToOffice:

    def test_assign_employee_to_office(self, db, client, create_user, create_company, create_office, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company)

        request_data = {'employee_id': employee.id}
        response = client.post(
            url_for('company.office_assign_employee', company_id=company.id, office_id=office.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 200

        db.session.refresh(employee)
        assert employee.office_id == office.id
        assert Employee.query.filter_by(id=employee.id, office_id=office.id).count() == 1

    def test_assign_already_assigned_employee_to_office(self, db, client, create_user, create_company, create_office,
                                                        create_employee, assign_employee_to_office):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company)
        assign_employee_to_office(office, employee)

        another_office = create_office(company)

        request_data = {'employee_id': employee.id}
        response = client.post(
            url_for('company.office_assign_employee', company_id=company.id, office_id=another_office.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 200

        db.session.refresh(employee)
        assert employee.office_id == another_office.id
        assert Employee.query.filter_by(id=employee.id, office_id=another_office.id).count() == 1
        assert Employee.query.filter_by(id=employee.id, office_id=office.id).count() == 0

    def test_assign_employee_to_office_without_authentication(self, db, client, create_user, create_company,
                                                              create_office, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company)

        request_data = {'employee_id': employee.id}
        response = client.post(
            url_for('company.office_assign_employee', company_id=company.id, office_id=office.id),
            json=request_data,
        )

        assert response.status_code == 401

    def test_assign_foreign_employee_to_office(self, db, client, create_user, create_company, create_office, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        another_owner = create_user(email='another_owner@gmail.com')
        another_company = create_company(another_owner)
        user = create_user()
        employee = create_employee(user, another_company)

        request_data = {'employee_id': employee.id}
        response = client.post(
            url_for('company.office_assign_employee', company_id=company.id, office_id=office.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 400

        db.session.refresh(employee)
        assert employee.office_id is None
        assert Employee.query.filter_by(id=employee.id, office_id=office.id).count() == 0

    def test_assign_employee_to_foreign_office(self, db, client, create_user, create_company, create_office,
                                               create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company)

        another_owner = create_user(email='another_owner@gmail.com')
        another_company = create_company(another_owner)
        another_office = create_office(another_company)

        request_data = {'employee_id': employee.id}
        response = client.post(
            url_for('company.office_assign_employee', company_id=company.id, office_id=another_office.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 403

        db.session.refresh(employee)
        assert employee.office_id is None
        assert Employee.query.filter_by(id=employee.id, office_id=office.id).count() == 0

    def test_assign_employee_to_not_existing_office(self, db, client, create_user, create_company, create_office,
                                                    create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        user = create_user()
        employee = create_employee(user, company)

        request_data = {'employee_id': employee.id}
        response = client.post(
            url_for('company.office_assign_employee', company_id=company.id, office_id=999),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 404

        db.session.refresh(employee)
        assert employee.office_id is None

    def test_assign_employee_to_office_of_non_existing_company(self, db, client, create_user, create_company, create_office,
                                                               create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company)

        request_data = {'employee_id': employee.id}
        response = client.post(
            url_for('company.office_assign_employee', company_id=999, office_id=office.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 404
