import datetime as dt

from sqlalchemy.orm import validates

from app.db import db
from common.utils import empty_string_to_none


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id', use_alter=True), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.now)

    employees = db.relationship(
        'User',
        foreign_keys='User.employer_id',
        backref=db.backref(
            'employer',
            uselist=False,
            lazy=True,
            cascade="all,delete",
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

    def is_owner(self, user):
        return self.owner_id == user.id
