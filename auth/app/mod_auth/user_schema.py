from marshmallow import Schema
from marshmallow import fields


class UserSchema(Schema):
    id = fields.String()
    email = fields.Email(required=True)
    created_at = fields.String()
