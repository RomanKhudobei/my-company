from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, abort

from company import services
from company.permissions import company_owner, company_owner_or_employee
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


class OfficeList(Resource):

    @jwt_required()
    @company_owner_or_employee('company_id')
    def get(self, company_id):
        company = services.get_company_by_id(company_id)

        if not company:
            abort(404)

        offices = services.get_company_offices(
            company=company,
            country_id=request.args.get('country_id'),
            region_id=request.args.get('region_id'),
            city_id=request.args.get('city_id'),
        )

        return OfficeSchema().dump(offices, many=True), 200


class OfficeRetrieve(Resource):

    @jwt_required()
    @company_owner('company_id')
    def get(self, company_id, office_id):
        company = services.get_company_by_id(company_id)

        if not company:
            abort(404)

        office = services.get_office_by_id(office_id)

        if not office:
            abort(404)

        return OfficeSchema().dump(office), 200


class OfficeUpdate(Resource):

    @jwt_required()
    @company_owner('company_id')
    def put(self, company_id, office_id):
        company = services.get_company_by_id(company_id)

        if not company:
            abort(404)

        office = services.get_office_by_id(office_id)

        if not office:
            abort(404)

        services.update_office(office, request.json)
        return OfficeSchema().dump(office), 200
