from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, abort

from company import services
from company.permissions import company_owner
from company.schemas.employee import EmployeeCreateSchema


class EmployeeCreate(Resource):

    @jwt_required()
    @company_owner('company_id')
    def post(self, company_id):
        company = services.get_company_by_id(company_id)

        if not company:
            abort(404)

        employee = services.create_employee(company, request.json.get('user_id'))
        return EmployeeCreateSchema().dump(employee), 201


class EmployeeList(Resource):

    @jwt_required()
    @company_owner('company_id')
    def get(self, company_id):
        company = services.get_company_by_id(company_id)

        if not company:
            abort(404)

        employees = services.get_company_employees(company.id, request.args.get('search'))
        return EmployeeCreateSchema(exclude=['user_id']).dump(employees, many=True), 200


class EmployeeRetrieve(Resource):

    @jwt_required()
    @company_owner('company_id')
    def get(self, company_id, employee_id):
        company = services.get_company_by_id(company_id)
        if not company:
            abort(404)

        employee = services.get_employee_by_id(employee_id)
        if not employee:
            abort(404)

        return EmployeeCreateSchema(exclude=['user_id']).dump(employee), 200


class EmployeeUpdate(Resource):

    @jwt_required()
    @company_owner('company_id')
    def put(self, company_id, employee_id):
        company = services.get_company_by_id(company_id)
        if not company:
            abort(404)

        employee = services.get_employee_by_id(employee_id)
        if not employee:
            abort(404)

        services.update_employee(employee, request.json)
        return EmployeeCreateSchema(exclude=['user_id']).dump(employee), 200


class EmployeeSetPassword(Resource):

    @jwt_required()
    @company_owner('company_id')
    def post(self, company_id, employee_id):
        company = services.get_company_by_id(company_id)
        if not company:
            abort(404)

        employee = services.get_employee_by_id(employee_id)
        if not employee:
            abort(404)

        if employee.company_id != company_id:
            abort(404)

        services.set_employee_password(employee, request.json.get('password'))
        return 200


class EmployeeDelete(Resource):

    @jwt_required()
    @company_owner('company_id')
    def delete(self, company_id, employee_id):
        company = services.get_company_by_id(company_id)
        if not company:
            abort(404)

        employee = services.get_employee_by_id(employee_id)
        if not employee:
            abort(404)

        services.delete_employee(employee)
        return 200
