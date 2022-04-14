import pytest
from flask import url_for

from company.models import Employee
from tests.e2e.auth.fixtures import get_auth_headers


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

        assert response.status_code == 404

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
