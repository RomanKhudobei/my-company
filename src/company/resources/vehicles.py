from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource, abort

from company import services
from company.permissions import company_owner
from company.schemas.vehicle import VehicleSchema


class VehicleCreate(Resource):

    @jwt_required()
    @company_owner('company_id')
    def post(self, company_id):
        company = services.get_company_by_id(company_id)

        if not company:
            abort(404)

        vehicle = services.create_vehicle(
            company=company,
            name=request.json.get('name'),
            model=request.json.get('model'),
            licence_plate=request.json.get('licence_plate'),
            year_of_manufacture=request.json.get('year_of_manufacture'),
            office_id=request.json.get('office_id'),
            driver_id=request.json.get('driver_id'),
        )

        return VehicleSchema().dump(vehicle), 201
