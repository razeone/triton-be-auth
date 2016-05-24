from marshmallow import Schema
from marshmallow import fields


class UserSchema(Schema):
    user_id = fields.UUID()
    email = fields.Email(required=True)
    is_active = fields.Boolean()
    is_admin = fields.Boolean()
    activation_token = fields.String()
    created_at = fields.DateTime()
    confirmated_at = fields.DateTime()
