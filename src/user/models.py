import datetime as dt

from sqlalchemy.orm import validates
from sqlalchemy_utils import EmailType, PasswordType

from app.db import db
from common.utils import empty_string_to_none


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(EmailType(), nullable=False, unique=True)
    password = db.Column(
        PasswordType(
            max_length=1024,
            schemes=['pbkdf2_sha512']
        ),
        nullable=False,
    )

    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.now)

    company = db.relationship(
        'Company',
        uselist=False,
        backref=db.backref(
            'owner',
            uselist=False,
            lazy=True,
            cascade="all,delete",
        )
    )

    def __repr__(self):
        return '<User ' \
               f'id={self.id} ' \
               f'email={self.email}' \
               '>'

    # not allow blank values on fields
    validates_first_name = validates('first_name')(lambda self, key, value: empty_string_to_none(value))
    validates_last_name = validates('last_name')(lambda self, key, value: empty_string_to_none(value))
    validates_email = validates('email')(lambda self, key, value: empty_string_to_none(value))
    validates_password = validates('password')(lambda self, key, value: empty_string_to_none(value))
