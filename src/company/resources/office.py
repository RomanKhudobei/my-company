from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, abort

from company import services
from company.permissions import company_owner
from company.schemas.office import OfficeSchema


class OfficeCreate(Resource):

    @jwt_required()
    @company_owner('company_id')
    def post(self, company_id):
        company = services.get_company_by_id(company_id)

        if not company:
            abort(404)

        office = services.create_office(
            company=company,
            name=request.json.get('name'),
            address=request.json.get('address'),
            country_id=request.json.get('country_id'),
            region_id=request.json.get('region_id'),
            city_id=request.json.get('city_id'),
        )

        return OfficeSchema().dump(office), 201
