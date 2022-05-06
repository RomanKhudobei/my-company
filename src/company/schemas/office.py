import marshmallow
from marshmallow import fields, validates

from app.marshmallow import ma
from common.marshmallow_validators import not_empty
from company.models import Office, Company
from location.models import Country, Region, City
from location.schemas import CountrySchema, RegionSchema, CitySchema


class OfficeSchema(ma.SQLAlchemyAutoSchema):
    name = fields.String(required=True, allow_none=False, validate=[not_empty])
    address = fields.String(required=True, allow_none=False, validate=[not_empty])

    id = fields.Integer(dump_only=True)
    country = fields.Nested(CountrySchema(), dump_only=True)
    region = fields.Nested(RegionSchema(), dump_only=True)
    city = fields.Nested(CitySchema(), dump_only=True)

    country_id = fields.Integer(required=True, allow_none=False, load_only=True)
    region_id = fields.Integer(required=True, allow_none=False, load_only=True)
    city_id = fields.Integer(required=True, allow_none=False, load_only=True)

    class Meta:
        model = Office
        include_fk = True
        include_relationships = True
        exclude = ['employees', 'company', 'vehicles']

    @validates('company_id')
    def validate_company_id(self, company_id):
        company = self.context.get('company') or Company.query.filter_by(id=company_id).one_or_none()

        if company is None:
            raise marshmallow.ValidationError(
                message='Company does not exist',
            )

    @validates('country_id')
    def validate_country_id(self, country_id):
        country = Country.query.filter_by(id=country_id).one_or_none()

        if country is None:
            raise marshmallow.ValidationError(
                message='Country does not exist.',
                field_name='country_id',
            )

        self.context['country'] = country

    @validates('region_id')
    def validate_region_id(self, region_id):
        region = Region.query.filter_by(id=region_id).one_or_none()

        if region is None:
            raise marshmallow.ValidationError(
                message='Region does not exist.',
                field_name='region_id',
            )

        self.context['region'] = region

    @validates('city_id')
    def validate_city_id(self, city_id):
        city = City.query.filter_by(id=city_id).one_or_none()

        if city is None:
            raise marshmallow.ValidationError(
                message='City does not exist.',
                field_name='city_id',
            )

        self.context['city'] = city

    @marshmallow.validates_schema(skip_on_field_errors=True)
    def validate_object(self, data, **kwargs):
        country, region, city = self.context.get('country'), self.context.get('region'), self.context.get('city')

        if region.country_id != country.id:
            raise marshmallow.ValidationError(
                message='Region does not belongs to country.',
                field_name='region_id',
            )

        if city.region_id != region.id:
            raise marshmallow.ValidationError(
                message='City does not belongs to region.',
                field_name='city_id',
            )
