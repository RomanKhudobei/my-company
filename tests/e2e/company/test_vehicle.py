import pytest
from flask import url_for

from tests.e2e.auth.fixtures import get_auth_headers


class TestVehicleCreate:

    def get_request_data(self, office_id=None, driver_id=None):
        data = {
            'name': 'Skoda',
            'model': 'Octavia',
            'licence_plate': 'AI 9999 EC',
            'year_of_manufacture': 2005,
        }

        if office_id:
            data['office_id'] = office_id

        if driver_id:
            data['driver_id'] = driver_id

        return data

    def test_create_vehicle(self, client, create_user, create_company, create_office, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company, office_id=office.id)

        request_data = self.get_request_data(office.id, user.id)
        response = client.post(
            url_for('company.vehicle_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 201

    def test_create_vehicle_with_missing_required_fields(self, client, create_user, create_company, create_office, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company, office_id=office.id)

        request_data = self.get_request_data(office.id, user.id)

        request_data['name'] = ''
        response = client.post(
            url_for('company.vehicle_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )
        assert response.status_code == 400

        request_data['name'] = None
        response = client.post(
            url_for('company.vehicle_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )
        assert response.status_code == 400

        del request_data['name']
        response = client.post(
            url_for('company.vehicle_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )
        assert response.status_code == 400

    def test_create_vehicle_with_missing_optional_fields(self, client, create_user, create_company, create_office, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company, office_id=office.id)

        request_data = self.get_request_data(office.id, user.id)

        request_data['office_id'] = None
        request_data['driver_id'] = None
        response = client.post(
            url_for('company.vehicle_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )
        assert response.status_code == 201

        del request_data['office_id']
        del request_data['driver_id']
        response = client.post(
            url_for('company.vehicle_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )
        assert response.status_code == 201

    def test_create_vehicle_without_authentication(self, client, create_user, create_company, create_office, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company, office_id=office.id)

        request_data = self.get_request_data(office.id, user.id)
        response = client.post(
            url_for('company.vehicle_create', company_id=company.id),
            json=request_data,
        )

        assert response.status_code == 401

    def test_create_vehicle_by_employee(self, client, create_user, create_company, create_office, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company)

        request_data = self.get_request_data(office.id, user.id)
        response = client.post(
            url_for('company.vehicle_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(user),
        )

        assert response.status_code == 403

    def test_create_vehicle_by_foreign_user(self, client, create_user, create_company, create_office, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        user = create_user()

        request_data = self.get_request_data(office.id, user.id)
        response = client.post(
            url_for('company.vehicle_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(user),
        )

        assert response.status_code == 403

    def test_create_vehicle_for_not_company_office(self, client, create_user, create_company, create_office,
                                                   create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        another_owner = create_user(email='another_owner@gmail.com')
        another_company = create_company(another_owner)
        office = create_office(another_company)

        user = create_user()
        employee = create_employee(user, company, office_id=office.id)

        request_data = self.get_request_data(office.id, user.id)
        response = client.post(
            url_for('company.vehicle_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 400

    def test_create_vehicle_for_not_employee(self, client, create_user, create_company, create_office, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        user = create_user()

        request_data = self.get_request_data(office.id, user.id)
        response = client.post(
            url_for('company.vehicle_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 400

    def test_create_vehicle_with_not_existing_driver(self, client, create_user, create_company, create_office,
                                                     create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company, office_id=office.id)

        request_data = self.get_request_data(office.id, 999)
        response = client.post(
            url_for('company.vehicle_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 400

    def test_create_vehicle_with_not_existing_office(self, client, create_user, create_company, create_office,
                                                     create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company, office_id=office.id)

        request_data = self.get_request_data(999, user.id)
        response = client.post(
            url_for('company.vehicle_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 400

    def test_create_vehicle_with_driver_from_different_offices(self, client, create_user, create_company, create_office,
                                                               create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)
        office1 = create_office(company)
        office2 = create_office(company)

        user = create_user()
        employee = create_employee(user, company, office_id=office1.id)

        request_data = self.get_request_data(office2.id, user.id)
        response = client.post(
            url_for('company.vehicle_create', company_id=company.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 400

    # TODO: add tests when one user has multiple vehicles


class TestVehicleList:

    def test_vehicle_list(self, client, create_user, create_company, create_vehicle):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        another_owner = create_user(email='another_owner@gmail.com')
        another_company = create_company(another_owner)

        vehicles_count = 5
        for _ in range(vehicles_count):
            create_vehicle(company)

        for _ in range(vehicles_count):
            create_vehicle(another_company)

        response = client.get(url_for('company.vehicle_list', company_id=company.id), headers=get_auth_headers(owner))

        assert response.status_code == 200
        assert len(response.json) == vehicles_count

    def test_vehicle_list_without_authentication(self, client, create_user, create_company, create_vehicle):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        another_owner = create_user(email='another_owner@gmail.com')
        another_company = create_company(another_owner)

        vehicles_count = 5
        for _ in range(vehicles_count):
            create_vehicle(company)

        for _ in range(vehicles_count):
            create_vehicle(another_company)

        response = client.get(url_for('company.vehicle_list', company_id=company.id))

        assert response.status_code == 401

    def test_vehicle_list_for_not_existing_company(self, client, create_user, create_company, create_vehicle):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        another_owner = create_user(email='another_owner@gmail.com')
        another_company = create_company(another_owner)

        vehicles_count = 5
        for _ in range(vehicles_count):
            create_vehicle(company)

        for _ in range(vehicles_count):
            create_vehicle(another_company)

        response = client.get(url_for('company.vehicle_list', company_id=999), headers=get_auth_headers(owner))

        assert response.status_code == 404

    def test_vehicle_list_by_foreign_owner(self, client, create_user, create_company, create_vehicle):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        another_owner = create_user(email='another_owner@gmail.com')
        another_company = create_company(another_owner)

        vehicles_count = 5
        for _ in range(vehicles_count):
            create_vehicle(company)

        for _ in range(vehicles_count):
            create_vehicle(another_company)

        response = client.get(url_for('company.vehicle_list', company_id=company.id), headers=get_auth_headers(another_owner))

        assert response.status_code == 403

    def test_vehicle_list_by_employee(self, client, create_user, create_company, create_vehicle, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        another_owner = create_user(email='another_owner@gmail.com')
        another_company = create_company(another_owner)

        user = create_user()
        employee = create_employee(user, company)

        vehicles_count = 5
        for _ in range(vehicles_count):
            create_vehicle(company)

        for _ in range(vehicles_count):
            create_vehicle(another_company)

        response = client.get(url_for('company.vehicle_list', company_id=company.id), headers=get_auth_headers(user))

        assert response.status_code == 403

    def test_vehicle_list_by_random_user(self, client, create_user, create_company, create_vehicle, create_employee):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        another_owner = create_user(email='another_owner@gmail.com')
        another_company = create_company(another_owner)

        user = create_user()

        vehicles_count = 5
        for _ in range(vehicles_count):
            create_vehicle(company)

        for _ in range(vehicles_count):
            create_vehicle(another_company)

        response = client.get(url_for('company.vehicle_list', company_id=company.id), headers=get_auth_headers(user))

        assert response.status_code == 403

    @pytest.mark.parametrize(
        'query,result_count',
        [
            ('', 6),
            ('?office_id=1', 2),
            ('?office_id=2', 3),
            ('?driver_id=1', 1),
            ('?driver_id=2', 2),
            ('?office_id=1&driver_id=1', 1),
            ('?office_id=2&driver_id=2', 2),
        ]
    )
    def test_vehicle_list_filters(self, client, create_user, create_company, create_vehicle, create_office,
                                  create_employee, query, result_count):
        user1 = create_user(email='user1@gmail.com')
        user2 = create_user(email='user2@gmail.com')

        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        another_owner = create_user(email='another_owner@gmail.com')
        another_company = create_company(another_owner)

        office1 = create_office(company)
        office2 = create_office(company)

        create_employee(user1, company, office_id=office1.id)
        create_employee(user2, company, office_id=office2.id)

        create_vehicle(company)
        create_vehicle(company, office_id=office1.id)
        create_vehicle(company, office_id=office2.id)
        create_vehicle(company, office_id=office1.id, driver_id=user1.id)
        create_vehicle(company, office_id=office2.id, driver_id=user2.id)
        create_vehicle(company, office_id=office2.id, driver_id=user2.id)

        for _ in range(5):
            create_vehicle(another_company)

        response = client.get(
            url_for('company.vehicle_list', company_id=company.id) + query,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 200
        assert len(response.json) == result_count


class TestVehicleRetrieve:

    def test_retrieve_vehicle(self, client, create_user, create_company, create_office, create_employee,
                              create_vehicle, assign_employee_to_office):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company)
        assign_employee_to_office(office, employee)

        vehicle = create_vehicle(company, office_id=office.id, driver_id=user.id)

        response = client.get(
            url_for('company.vehicle_retrieve', company_id=company.id, vehicle_id=vehicle.id),
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 200
        assert response.json.get('id') == vehicle.id

    def test_retrieve_vehicle_without_authentication(self, client, create_user, create_company, create_office, create_employee,
                                                     create_vehicle, assign_employee_to_office):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company)
        assign_employee_to_office(office, employee)

        vehicle = create_vehicle(company, office_id=office.id, driver_id=user.id)

        response = client.get(
            url_for('company.vehicle_retrieve', company_id=company.id, vehicle_id=vehicle.id),
        )

        assert response.status_code == 401

    def test_retrieve_non_existing_vehicle(self, client, create_user, create_company, create_office, create_employee,
                                           create_vehicle, assign_employee_to_office):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company)
        assign_employee_to_office(office, employee)

        vehicle = create_vehicle(company, office_id=office.id, driver_id=user.id)

        response = client.get(
            url_for('company.vehicle_retrieve', company_id=company.id, vehicle_id=999),
            headers=get_auth_headers(owner),
        )
        assert response.status_code == 404

    def test_retrieve_not_company_vehicle(self, client, create_user, create_company, create_office, create_employee,
                                          create_vehicle, assign_employee_to_office):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        owner2 = create_user(email='owner2@gmail.com')
        company2 = create_company(owner2)

        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company)
        assign_employee_to_office(office, employee)

        vehicle = create_vehicle(company, office_id=office.id, driver_id=user.id)

        response = client.get(
            url_for('company.vehicle_retrieve', company_id=company2.id, vehicle_id=vehicle.id),
            headers=get_auth_headers(owner2),
        )
        assert response.status_code == 404


class TestVehicleUpdate:

    def test_update_vehicle(self, client, create_user, create_company, create_office, create_employee, create_vehicle,
                            assign_employee_to_office, db):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company)
        assign_employee_to_office(office, employee)

        vehicle = create_vehicle(company, office_id=office.id, driver_id=user.id)

        new_office = create_office(company)

        new_driver = create_user(email='newdriver@gmail.com')
        employee = create_employee(new_driver, company)
        assign_employee_to_office(new_office, employee)

        request_data = {
            'name': vehicle.name,
            'model': 'Fabia',
            'licence_plate': vehicle.licence_plate,
            'year_of_manufacture': vehicle.year_of_manufacture,
            'office_id': new_office.id,
            'driver_id': new_driver.id,
        }

        response = client.put(
            url_for('company.vehicle_update', company_id=company.id, vehicle_id=vehicle.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 200
        db.session.refresh(vehicle)

        assert vehicle.model == 'Fabia'
        assert vehicle.office_id == new_office.id
        assert vehicle.driver_id == new_driver.id

    def test_update_vehicle_company_id(self, client, create_user, create_company, create_office, create_employee, create_vehicle,
                                       assign_employee_to_office, db):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company)
        assign_employee_to_office(office, employee)

        vehicle = create_vehicle(company, office_id=office.id, driver_id=user.id)

        request_data = {
            'company_id': 999,
            'name': vehicle.name,
            'model': 'Fabia',
            'licence_plate': vehicle.licence_plate,
            'year_of_manufacture': vehicle.year_of_manufacture,
            'office_id': office.id,
            'driver_id': user.id,
        }

        response = client.put(
            url_for('company.vehicle_update', company_id=company.id, vehicle_id=vehicle.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 400

    def test_update_vehicle_remove_office_and_driver(self, client, create_user, create_company, create_office,
                                                     create_employee, create_vehicle,
                                                     assign_employee_to_office, db):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company)
        assign_employee_to_office(office, employee)

        vehicle = create_vehicle(company, office_id=office.id, driver_id=user.id)

        request_data = {
            'name': vehicle.name,
            'model': 'Fabia',
            'licence_plate': vehicle.licence_plate,
            'year_of_manufacture': vehicle.year_of_manufacture,
            'office_id': None,
            'driver_id': None,
        }

        response = client.put(
            url_for('company.vehicle_update', company_id=company.id, vehicle_id=vehicle.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 200

        db.session.refresh(vehicle)
        assert vehicle.office_id is None
        assert vehicle.driver_id is None

    def test_update_vehicle_set_employee_from_different_office(self, client, create_user, create_company, create_office,
                                                               create_employee, create_vehicle,
                                                               assign_employee_to_office, db):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company)
        assign_employee_to_office(office, employee)

        vehicle = create_vehicle(company, office_id=office.id, driver_id=user.id)

        new_office = create_office(company)

        request_data = {
            'name': vehicle.name,
            'model': 'Fabia',
            'licence_plate': vehicle.licence_plate,
            'year_of_manufacture': vehicle.year_of_manufacture,
            'office_id': new_office.id,
            'driver_id': user.id,
        }

        response = client.put(
            url_for('company.vehicle_update', company_id=company.id, vehicle_id=vehicle.id),
            json=request_data,
            headers=get_auth_headers(owner),
        )

        assert response.status_code == 400

    def test_update_vehicle_that_belongs_to_another_company(self, client, create_user, create_company, create_office,
                                                            create_employee, create_vehicle,
                                                            assign_employee_to_office, db):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        owner2 = create_user(email='owner2@gmail.com')
        company2 = create_company(owner2)

        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company)
        assign_employee_to_office(office, employee)

        vehicle = create_vehicle(company, office_id=office.id, driver_id=user.id)

        request_data = {
            'name': vehicle.name,
            'model': 'Fabia',
            'licence_plate': vehicle.licence_plate,
            'year_of_manufacture': vehicle.year_of_manufacture,
            'office_id': office.id,
            'driver_id': user.id,
        }

        response = client.put(
            url_for('company.vehicle_update', company_id=company.id, vehicle_id=vehicle.id),
            json=request_data,
            headers=get_auth_headers(owner2),
        )

        assert response.status_code == 403

    def test_update_non_exiting_company_vehicle(self, client, create_user, create_company, create_office,
                                                create_employee, create_vehicle,
                                                assign_employee_to_office, db):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        owner2 = create_user(email='owner2@gmail.com')
        company2 = create_company(owner2)

        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company)
        assign_employee_to_office(office, employee)

        vehicle = create_vehicle(company, office_id=office.id, driver_id=user.id)

        request_data = {
            'name': vehicle.name,
            'model': 'Fabia',
            'licence_plate': vehicle.licence_plate,
            'year_of_manufacture': vehicle.year_of_manufacture,
            'office_id': office.id,
            'driver_id': user.id,
        }

        response = client.put(
            url_for('company.vehicle_update', company_id=company2.id, vehicle_id=vehicle.id),
            json=request_data,
            headers=get_auth_headers(owner2),
        )

        assert response.status_code == 404

    def test_update_vehicle_without_authentication(self, client, create_user, create_company, create_office,
                                                   create_employee, create_vehicle,
                                                   assign_employee_to_office, db):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company)
        assign_employee_to_office(office, employee)

        vehicle = create_vehicle(company, office_id=office.id, driver_id=user.id)

        request_data = {
            'name': vehicle.name,
            'model': 'Fabia',
            'licence_plate': vehicle.licence_plate,
            'year_of_manufacture': vehicle.year_of_manufacture,
            'office_id': office.id,
            'driver_id': user.id,
        }

        response = client.put(
            url_for('company.vehicle_update', company_id=company.id, vehicle_id=vehicle.id),
            json=request_data,
        )

        assert response.status_code == 401

    def test_update_vehicle_by_driver(self, client, create_user, create_company, create_office,
                                      create_employee, create_vehicle,
                                      assign_employee_to_office, db):
        owner = create_user(email='owner@gmail.com')
        company = create_company(owner)

        office = create_office(company)

        user = create_user()
        employee = create_employee(user, company)
        assign_employee_to_office(office, employee)

        vehicle = create_vehicle(company, office_id=office.id, driver_id=user.id)

        request_data = {
            'name': vehicle.name,
            'model': 'Fabia',
            'licence_plate': vehicle.licence_plate,
            'year_of_manufacture': vehicle.year_of_manufacture,
            'office_id': office.id,
            'driver_id': user.id,
        }

        response = client.put(
            url_for('company.vehicle_update', company_id=company.id, vehicle_id=vehicle.id),
            json=request_data,
            headers=get_auth_headers(user)
        )

        assert response.status_code == 403
