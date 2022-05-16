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


class VehicleList(Resource):

    @jwt_required()
    @company_owner('company_id')
    def get(self, company_id):
        company = services.get_company_by_id(company_id)

        if not company:
            abort(404)

        vehicles = services.get_company_vehicles(
            company=company,
            office_id=request.args.get('office_id'),
            driver_id=request.args.get('driver_id'),
        )

        return VehicleSchema().dump(vehicles, many=True), 200


class VehicleRetrieve(Resource):

    @jwt_required()
    @company_owner('company_id')
    def get(self, company_id, vehicle_id):
        company = services.get_company_by_id(company_id)

        if not company:
            abort(404)

        vehicle = services.get_vehicle_by_id(vehicle_id)

        if vehicle is None:
            abort(404)

        if vehicle.company_id != company.id:
            abort(404)

        return VehicleSchema().dump(vehicle), 200


class VehicleUpdate(Resource):

    @jwt_required()
    @company_owner('company_id')
    def put(self, company_id, vehicle_id):
        company = services.get_company_by_id(company_id)

        if not company:
            abort(404)

        vehicle = services.get_vehicle_by_id(vehicle_id)

        if vehicle is None:
            abort(404)

        if vehicle.company_id != company.id:
            abort(404)

        services.update_vehicle(vehicle, request.json)
        return VehicleSchema().dump(vehicle), 200
