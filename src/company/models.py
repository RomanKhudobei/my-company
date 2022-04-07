import datetime as dt

from sqlalchemy.orm import validates

from app.db import db
from common.utils import empty_string_to_none


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.now)

    def __repr__(self):
        return '<Company ' \
               f'{self.id=} ' \
               f'{self.name=} ' \
               f'{self.owner_id=}' \
               '>'

    # not allow blank values on fields
    validates_name = validates('name')(lambda self, key, value: empty_string_to_none(value))
