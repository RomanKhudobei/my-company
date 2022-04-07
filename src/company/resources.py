from flask import request
from flask_jwt_extended import jwt_required, current_user
from flask_restful import Resource

from company import services
from company.schemas import CompanySchema


class CompanyCreate(Resource):

    @jwt_required()
    def post(self):
        company = services.register_company(
            user=current_user,
            name=request.json.get('company_name'),
        )

        return {'company': CompanySchema().dump(company)}, 201
