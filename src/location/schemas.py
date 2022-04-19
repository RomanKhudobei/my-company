from app.marshmallow import ma
from location.models import Country, Region, City


class CountrySchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Country


class RegionSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Region


class CitySchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = City
