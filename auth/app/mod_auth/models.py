from app import db
from sqlalchemy_utils import UUIDType
from flask.ext.login import UserMixin
import datetime


class User(UserMixin, db.Model):

    __tablename__ = 'user'

    user_id = db.Column(UUIDType, unique=True, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    activation_token = db.Column(db.String(128), unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    confirmated_at = db.Column(db.DateTime)
    password = db.Column(db.String(192), nullable=False)

    def __init__(self, user_id, email, password, activation_token):
        self.user_id = user_id
        self.activation_token = activation_token
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User(email={self.email!r})'.format(self=self)
