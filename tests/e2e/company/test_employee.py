import pytest
from flask import url_for

from app.db import db
from company.models import Employee
from tests.e2e.auth.fixtures import get_auth_headers
from user.models import User


class TestEmployeeCreate:

    def test_employee_create(self, client, create_user, create_company):
        owner = create_user()
        company = create_company(owner)

        user = create_user(email='employee@gmail.com')

        request_data = {'user_id': user.id}
        response = client.post(
            url_for('company.employee_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner)
        )

        assert response.status_code == 201

        assert Employee.query.filter_by(user_id=user.id, company_id=company.id).one_or_none()
        assert len(company.employees) == 1
        assert user.employer.id == company.id

    def test_employee_create_already_employed(self, client, create_user, create_company):
        owner = create_user()
        company = create_company(owner)

        user = create_user(email='employee@gmail.com')

        request_data = {'user_id': user.id}
        response = client.post(
            url_for('company.employee_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner)
        )

        response = client.post(
            url_for('company.employee_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner)
        )

        assert response.status_code == 400

    def test_employee_create_not_by_owner(self, client, create_user, create_company):
        owner = create_user()
        company = create_company(owner)

        user = create_user(email='employee@gmail.com')

        request_data = {'user_id': user.id}
        response = client.post(
            url_for('company.employee_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(user)
        )

        assert response.status_code == 403

    def test_employee_create_user_not_exist(self, client, create_user, create_company):
        owner = create_user()
        company = create_company(owner)

        request_data = {'user_id': 999}
        response = client.post(
            url_for('company.employee_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner)
        )

        assert response.status_code == 400

    def test_create_owner_as_employee(self, client, create_user, create_company):
        owner = create_user()
        company = create_company(owner)

        request_data = {'user_id': owner.id}
        response = client.post(
            url_for('company.employee_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner)
        )

        assert response.status_code == 400

    def test_create_owner_of_another_company_as_employee(self, client, create_user, create_company):
        owner = create_user()
        company = create_company(owner)

        another_owner = create_user(email='another_owner@gmail.com')
        create_company(another_owner)

        request_data = {'user_id': another_owner.id}
        response = client.post(
            url_for('company.employee_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner)
        )

        assert response.status_code == 400


class TestEmployeeList:

    def test_employee_list(self, client, create_user, create_company, create_employee):
        users1 = [create_user(email=f'test1{i}@gmail.com') for i in range(5)]
        users2 = [create_user(email=f'test2{i}@gmail.com') for i in range(5)]

        owner1 = create_user(email='owner1@gmail.com')
        owner2 = create_user(email='owner2@gmail.com')
        company1 = create_company(owner1)
        company2 = create_company(owner2)

        for user in users1:
            create_employee(user, company1)

        for user in users2:
            create_employee(user, company2)

        response = client.get(
            url_for('company.employee_list', company_id=company1.id),
            headers=get_auth_headers(owner1),
        )

        assert response.status_code == 200

        assert len(response.json) == len(users1)

    @pytest.mark.parametrize(
        'query,result_count',
        [
            ('', 3),
            ('test', 0),
            ('John', 2),
            ('Doe', 1),
            ('smith', 1),
            ('leclerc', 1),
        ]
    )
    def test_employee_list_search(self, client, create_user, create_company, create_employee, query, result_count):
        users = [
            create_user(
                first_name='John',
                last_name='Doe',
                email='john.doe@gmail.com',
            ),
            create_user(
                first_name='Johnathan',
                last_name='Smith',
                email='john.smith@gmail.com',
            ),
            create_user(
                first_name='Charles',
                last_name='Leclerc',
                email='c.leclerc@gmail.com',
            ),
        ]

        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        for user in users:
            create_employee(user, company)

        response = client.get(
            url_for('company.employee_list', company_id=company.id) + f'?search={query}',
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 200

        assert len(response.json) == result_count

    def test_employee_list_search_with_wrong_parameter(self, client, create_user, create_company, create_employee):
        users = [
            create_user(
                first_name='John',
                last_name='Doe',
                email='john.doe@gmail.com',
            ),
            create_user(
                first_name='Johnathan',
                last_name='Smith',
                email='john.smith@gmail.com',
            ),
            create_user(
                first_name='Charles',
                last_name='Leclerc',
                email='c.leclerc@gmail.com',
            ),
        ]

        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        for user in users:
            create_employee(user, company)

        response = client.get(
            url_for('company.employee_list', company_id=company.id) + f'?invalid=john',
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 200

        assert len(response.json) == 3


class TestEmployeeRetrieve:

    def test_employee_retrieve(self, client, create_user, create_company, create_employee):
        user = create_user()
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        employee = create_employee(user, company)

        response = client.get(
            url_for('company.employee_retrieve', company_id=company.id, employee_id=employee.id),
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 200
        assert response.json.get('id') == employee.id

    def test_employee_retrieve_without_authentication(self, client, create_user, create_company, create_employee):
        user = create_user()
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        employee = create_employee(user, company)

        response = client.get(
            url_for('company.employee_retrieve', company_id=company.id, employee_id=employee.id),
        )

        assert response.status_code == 401

    def test_employee_retrieve_not_exist(self, client, create_user, create_company, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        response = client.get(
            url_for('company.employee_retrieve', company_id=company.id, employee_id=999),
            headers=get_auth_headers(owner)
        )

        assert response.status_code == 404

    def test_employee_retrieve_company_not_exist(self, client, create_user, create_company, create_employee):
        owner = create_user(email='owner@gmail.com')
        response = client.get(
            url_for('company.employee_retrieve', company_id=999, employee_id=999),
            headers=get_auth_headers(owner)
        )

        assert response.status_code == 404

    def test_employee_retrieve_not_by_company_owner(self, client, create_user, create_company, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        another_owner = create_user(email='another_owner@gmail.com')
        another_company = create_company(another_owner)

        user = create_user()
        employee = create_employee(user, company)

        response = client.get(
            url_for('company.employee_retrieve', company_id=company.id, employee_id=employee.id),
            headers=get_auth_headers(another_owner)
        )

        assert response.status_code == 403


class TestEmployeeUpdate:

    def test_employee_update(self, client, create_user, create_company, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        user = create_user()
        employee = create_employee(user, company)
        request_data = {
            'first_name': 'updated',
            'last_name': 'updated',
        }
        response = client.put(
            url_for('company.employee_update', company_id=company.id, employee_id=employee.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 200

        db.session.refresh(employee)

        assert employee.user.first_name == 'updated'
        assert employee.user.last_name == 'updated'

    def test_employee_update_email(self, client, create_user, create_company, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        user = create_user()
        employee = create_employee(user, company)
        request_data = {
            'first_name': 'updated',
            'last_name': 'updated',
            'email': 'updated@gmail.com'
        }
        response = client.put(
            url_for('company.employee_update', company_id=company.id, employee_id=employee.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 400

    def test_employee_update_password(self, client, create_user, create_company, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        user = create_user()
        employee = create_employee(user, company)
        request_data = {
            'first_name': 'updated',
            'last_name': 'updated',
            'password': 'qwerty123'
        }
        response = client.put(
            url_for('company.employee_update', company_id=company.id, employee_id=employee.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 400

    def test_employee_update_employer(self, client, create_user, create_company, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        user = create_user()
        employee = create_employee(user, company)
        request_data = {
            'first_name': 'updated',
            'last_name': 'updated',
            'employer': 999,
        }
        response = client.put(
            url_for('company.employee_update', company_id=company.id, employee_id=employee.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 400

    def test_employee_update_without_authentication(self, client, create_user, create_company, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        user = create_user()
        employee = create_employee(user, company)
        request_data = {
            'first_name': 'updated',
            'last_name': 'updated',
        }
        response = client.put(
            url_for('company.employee_update', company_id=company.id, employee_id=employee.id),
            json=request_data,
        )

        assert response.status_code == 401

    def test_employee_update_not_by_employer(self, client, create_user, create_company, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        another_owner = create_user(email='another_owner@gmail.com')
        another_company = create_company(another_owner)

        user = create_user()
        employee = create_employee(user, company)
        request_data = {
            'first_name': 'updated',
            'last_name': 'updated',
        }
        response = client.put(
            url_for('company.employee_update', company_id=company.id, employee_id=employee.id),
            json=request_data,
            headers=get_auth_headers(another_owner),
        )

        assert response.status_code == 403

    def test_employee_update_by_employee_himself(self, client, create_user, create_company, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        user = create_user()
        employee = create_employee(user, company)
        request_data = {
            'first_name': 'updated',
            'last_name': 'updated',
        }
        response = client.put(
            url_for('company.employee_update', company_id=company.id, employee_id=employee.id),
            json=request_data,
            headers=get_auth_headers(user),
        )

        assert response.status_code == 403


class TestEmployeeDelete:

    def test_employee_delete(self, client, create_user, create_company, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        user = create_user()
        employee = create_employee(user, company)

        response = client.delete(
            url_for('company.employee_delete', company_id=company.id, employee_id=employee.id),
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 200
        assert Employee.query.filter_by(company_id=company.id, user_id=user.id).count() == 0
        assert User.query.count() == 1  # only owner left after employee deletion

    def test_employee_delete_without_authentication(self, client, create_user, create_company, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        user = create_user()
        employee = create_employee(user, company)

        response = client.delete(
            url_for('company.employee_delete', company_id=company.id, employee_id=employee.id),
        )

        assert response.status_code == 401

    def test_employee_delete_not_by_employer(self, client, create_user, create_company, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        user = create_user()
        employee = create_employee(user, company)

        another_owner = create_user(email='another_owner@gmail.com')
        another_company = create_company(another_owner)

        response = client.delete(
            url_for('company.employee_delete', company_id=company.id, employee_id=employee.id),
            headers=get_auth_headers(another_owner),
        )

        assert response.status_code == 403

    def test_employee_delete_by_himself(self, client, create_user, create_company, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        user = create_user()
        employee = create_employee(user, company)

        response = client.delete(
            url_for('company.employee_delete', company_id=company.id, employee_id=employee.id),
            headers=get_auth_headers(user),
        )

        assert response.status_code == 403

    def test_delete_not_existing_employee(self, client, create_user, create_company, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        response = client.delete(
            url_for('company.employee_delete', company_id=company.id, employee_id=999),
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 404

    def test_employee_delete_from_not_existing_company(self, client, create_user, create_company, create_employee):
        owner = create_user(email='owner@gmail.com')

        response = client.delete(
            url_for('company.employee_delete', company_id=999, employee_id=999),
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 404
