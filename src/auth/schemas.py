from marshmallow import fields

from app.marshmallow import ma
from common.marshmallow_validators import not_empty


class UserLoginSchema(ma.Schema):
    email = fields.Email(required=True, allow_none=False)
    password = fields.String(required=True, allow_none=False, validate=[not_empty])
