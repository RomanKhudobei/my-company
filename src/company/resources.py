from flask import request
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource, abort

from company import services
from company.schemas import CompanySchema


class CompanyCreate(Resource):

    @jwt_required()
    def post(self):
        company = services.register_company(
            user=current_user,
            name=request.json.get('name'),
        )

        return CompanySchema().dump(company), 201


class CompanyRetrieve(Resource):

    @jwt_required()
    def get(self, company_id):
        company = services.get_company_by_id(company_id)

        if not company:
            abort(404)

        if current_user.id != company.owner_id:
            abort(403)

        response_data = {}

        if company:
            response_data = CompanySchema().dump(company)

        return response_data, 200


class CompanyUpdate(Resource):

    @jwt_required()
    def put(self, company_id):
        company = services.get_company_by_id(company_id)

        if not company:
            abort(404)

        if not company.is_owner(current_user):
            abort(403)

        services.update_company(company, request.json)
        return CompanySchema().dump(company), 200
