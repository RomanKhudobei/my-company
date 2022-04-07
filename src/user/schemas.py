import marshmallow
from marshmallow import fields, validates

from app.marshmallow import ma
from common.marshmallow_validators import not_empty
from user.models import User


class UserCreateSchema(ma.Schema):
    first_name = fields.String(required=True, allow_none=False, validate=[not_empty])
    last_name = fields.String(required=True, allow_none=False, validate=[not_empty])
    email = fields.Email(required=True, allow_none=False)
    password = fields.String(required=True, allow_none=False, validate=[not_empty])
    repeat_password = fields.String(required=True, allow_none=False, validate=[not_empty])

    @validates('email')
    def validate_email(self, email):
        user_already_exist = User.query.filter_by(email=email).first() is not None
        if user_already_exist:
            raise marshmallow.ValidationError(
                message=f'User with email "{email}" already exist',
                field_name='email',
            )

    @marshmallow.validates_schema(skip_on_field_errors=True)
    def validate_object(self, data, **kwargs):
        if data['password'] < data['repeat_password']:
            raise marshmallow.ValidationError(
                message='Passwords not match',
                field_name='repeat_password',
            )


class UserSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = User
        # include_fk = True
        include_relationships = True
        exclude = ['password']
