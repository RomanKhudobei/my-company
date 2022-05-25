import datetime as dt

from sqlalchemy.orm import validates

from app.db import db
from common.utils import empty_string_to_none


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.now)

    owner = db.relationship(  # load joined?
        'User',
        uselist=False,
        cascade="all,delete",
        backref=db.backref(
            'company',
            uselist=False,
            lazy=True,
        )
    )

    def __repr__(self):
        return '<Company ' \
               f'id={self.id} ' \
               f'name={self.name} ' \
               f'owner_id={self.owner_id}' \
               '>'

    # not allow blank values on fields
    validates_name = validates('name')(lambda self, key, value: empty_string_to_none(value))


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey('office.id', ondelete='SET NULL'))

    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.now)

    user = db.relationship(
        'User',
        uselist=False,
        cascade='all,delete',
        backref=db.backref(
            'employer',
            uselist=False,
            lazy=True,
        )
    )
    company = db.relationship(
        'Company',
        uselist=False,
        backref=db.backref(
            'employees',
            lazy=True,
            cascade="all,delete",
        )
    )
    office = db.relationship(
        'Office',
        uselist=False,
        backref=db.backref(
            'employees',
            lazy=True,
        )
    )


class Office(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    company = db.relationship(
        'Company',
        uselist=False,
        backref=db.backref(
            'offices',
            lazy=True,
            cascade='all,delete',
        ),
    )

    country_id = db.Column(db.Integer, db.ForeignKey('country.id', ondelete='SET NULL'))
    region_id = db.Column(db.Integer, db.ForeignKey('region.id', ondelete='SET NULL'))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id', ondelete='SET NULL'))

    # country = db.relationship(
    #     'Country',
    #     uselist=False,
    #     backref=db.backref(
    #         'offices',
    #         lazy=True,
    #     )
    # )
    # region = db.relationship(
    #     'Region',
    #     uselist=False,
    #     backref=db.backref(
    #         'offices',
    #         lazy=True,
    #     )
    # )
    # city = db.relationship(
    #     'City',
    #     uselist=False,
    #     backref=db.backref(
    #         'offices',
    #         lazy=True,
    #     )
    # )

    # not allow blank values on fields
    validates_name = validates('name')(lambda self, key, value: empty_string_to_none(value))
    validates_address = validates('address')(lambda self, key, value: empty_string_to_none(value))


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    model = db.Column(db.String, nullable=False)
    licence_plate = db.Column(db.String, nullable=False)
    year_of_manufacture = db.Column(db.SmallInteger, nullable=False)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    office_id = db.Column(db.Integer, db.ForeignKey('office.id', ondelete='SET NULL'))
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))

    company = db.relationship(
        'Company',
        uselist=False,
        backref=db.backref(
            'vehicles',
            lazy=True,
            cascade='all,delete',
        ),
    )
    office = db.relationship(
        'Office',
        uselist=False,
        backref=db.backref(
            'vehicles',
            lazy=True,
        ),
    )
    driver = db.relationship(
        'User',
        uselist=False,
        backref=db.backref(
            'vehicles',
            lazy=True,
        ),
    )

    # not allow blank values on fields
    validates_name = validates('name')(lambda self, key, value: empty_string_to_none(value))
    validates_model = validates('model')(lambda self, key, value: empty_string_to_none(value))
    validates_licence_plate = validates('licence_plate')(lambda self, key, value: empty_string_to_none(value))
