from sqlalchemy.orm import validates

from app.db import db
from common.utils import empty_string_to_none


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    regions = db.relationship(
        'Region',
        cascade='all,delete',
        backref=db.backref(
            'country',
            uselist=False,
            lazy=True,
        )
    )

    offices = db.relationship(
        'Office',
        backref=db.backref(
            'country',
            uselist=False,
            lazy=True,
        )
    )

    # not allow blank values on fields
    validates_name = validates('name')(lambda self, key, value: empty_string_to_none(value))


class Region(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)

    cities = db.relationship(
        'City',
        cascade='all,delete',
        backref=db.backref(
            'region',
            uselist=False,
            lazy=True,
        )
    )

    offices = db.relationship(
        'Office',
        backref=db.backref(
            'region',
            uselist=False,
            lazy=True,
        )
    )

    # not allow blank values on fields
    validates_name = validates('name')(lambda self, key, value: empty_string_to_none(value))


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)

    offices = db.relationship(
        'Office',
        backref=db.backref(
            'city',
            uselist=False,
            lazy=True,
        )
    )

    # not allow blank values on fields
    validates_name = validates('name')(lambda self, key, value: empty_string_to_none(value))
