from marshmallow import validate


not_empty = validate.Length(min=1)
