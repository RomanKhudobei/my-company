"""empty message

Revision ID: create_locations
Revises: ce9e5728ed3c
Create Date: 2022-05-19 12:40:00.786464

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base


# revision identifiers, used by Alembic.
revision = 'create_locations'
down_revision = 'ce9e5728ed3c'
branch_labels = None
depends_on = None

Base = declarative_base()


class Country(Base):
    __tablename__ = 'country'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)


class Region(Base):
    __tablename__ = 'region'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    country_id = sa.Column(sa.Integer, sa.ForeignKey('country.id'), nullable=False)


class City(Base):
    __tablename__ = 'city'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    region_id = sa.Column(sa.Integer, sa.ForeignKey('region.id'), nullable=False)


LOCATIONS = {
    'Ukraine': {
        'Kiyv oblast': ['Kyiv'],
        'Kharkiv oblast': ['Kharkiv'],
        'Lviv oblast': ['Lviv'],
        'Ternopil oblast': ['Ternopil'],
        # ...
    },
    'USA': {
        'Ohio': ['Columbus'],
        'Texas': ['Austin'],
        'California': ['Sacramento'],
        'Kansas': ['Topeka'],
        # ...
    },
    'Poland': {
        'Greater Poland': ['Poznań'],
        'Lesser Poland': ['Kraków'],
        'Łódź': ['Łódź'],
        'Lower Silesia': ['Wrocław'],
        # ...
    },
    # ...
}


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    countries = []
    for country in LOCATIONS.keys():
        countries.append(Country(name=country))

    session.add_all(countries)
    session.commit()

    country_to_regions = {}
    for country in countries:
        country_to_regions.setdefault(country.name, [])

        for region in LOCATIONS[country.name]:
            country_to_regions[country.name].append(Region(name=region, country_id=country.id))

        session.add_all(country_to_regions[country.name])

    session.commit()

    cities = []
    for country_name, regions in country_to_regions.items():
        for region in regions:
            for city in LOCATIONS[country_name][region.name]:
                cities.append(City(name=city, region_id=region.id))

    session.add_all(cities)
    session.commit()


def downgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    Country.query.delete()
    Region.query.delete()
    City.query.delete()

    session.commit()
