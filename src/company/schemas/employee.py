import marshmallow
from marshmallow import fields, validates

from app.marshmallow import ma
from company.models import Employee
from user.models import User


class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        model = Employee
        include_fk = True

    @validates('user_id')
    def validate_user_id(self, user_id):
        user = User.query.filter_by(id=user_id).one_or_none()

        if user is None:
            raise marshmallow.ValidationError(
                message='User does not exist.',
                field_name='user_id',
            )

        if user.employer is not None:
            raise marshmallow.ValidationError(
                message='User already employed',
                field_name='user_id',
            )
