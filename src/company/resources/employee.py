from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, abort

from company import services
from company.permissions import company_owner
from company.schemas.employee import EmployeeSchema


class EmployeeCreate(Resource):

    @jwt_required()
    @company_owner('company_id')
    def post(self, company_id):
        company = services.get_company_by_id(company_id)

        if not company:
            abort(404)

        employee = services.create_employee(company, request.json.get('user_id'))
        return EmployeeSchema().dump(employee), 201


class EmployeeList(Resource):

    @jwt_required()
    @company_owner('company_id')
    def get(self, company_id):
        company = services.get_company_by_id(company_id)

        if not company:
            abort(404)

        employees = services.get_company_employees(company.id, request.args.get('search'))
        return EmployeeSchema(exclude=['user_id']).dump(employees, many=True), 200
