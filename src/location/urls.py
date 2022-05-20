from flask import Blueprint
from flask_restful import Api

from location.resources import CountryList, RegionList, CityList

bp = Blueprint('location', __name__)
api = Api(bp)

api.add_resource(CountryList, '/countries/', endpoint='country_list')
api.add_resource(RegionList, '/countries/<int:country_id>/regions/', endpoint='region_list')
api.add_resource(CityList, '/countries/<int:country_id>/regions/<int:region_id>/cities/', endpoint='city_list')
