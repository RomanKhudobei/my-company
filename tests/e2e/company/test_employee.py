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
