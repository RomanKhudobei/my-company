from flask_restful import Resource, abort

from location import services
from location.schemas import CountrySchema, RegionSchema, CitySchema


class CountryList(Resource):

    def get(self):
        countries = services.get_countries()
        return CountrySchema().dump(countries, many=True), 200


class RegionList(Resource):

    def get(self, country_id):
        country = services.get_country_by_id(country_id)

        if not country:
            abort(404)

        regions = services.get_country_regions(country.id)
        return RegionSchema().dump(regions, many=True), 200


class CityList(Resource):

    def get(self, country_id, region_id):
        country = services.get_country_by_id(country_id)

        if not country:
            abort(404)

        region = services.get_region_by_id(region_id)

        if not region:
            abort(404)

        cities = services.get_region_cities(region.id)
        return CitySchema().dump(cities, many=True), 200
