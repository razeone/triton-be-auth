from marshmallow import Schema
from marshmallow import fields
from marshmallow import ValidationError


class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    email = fields.Str()
    created_at = fields.Str()
