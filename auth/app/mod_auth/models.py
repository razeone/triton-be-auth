from datetime import datetime

from sqlalchemy_utils import UUIDType
from flask.ext.login import UserMixin

from app import db


class User(UserMixin, db.Model):

    __tablename__ = 'user'

    user_id = db.Column(UUIDType, unique=True, primary_key=True)
    email = db.Column(db.String(128), nullable=False)
    social_id = db.Column(db.String(100))
    social_network = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    activation_token = db.Column(db.String(128), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmated_at = db.Column(db.DateTime)
    password = db.Column(db.String(192), nullable=False)

    def __init__(self, user_id, email="", password="", social_id=None, social_network=None, activation_token=None):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.social_id = social_id
        self.social_network = social_network
        self.activation_token = activation_token
        if social_id is not None:
            self.is_active = True
            self.confirmated_at = datetime.utcnow()

    def get_id(self):
        return self.user_id

    def __repr__(self):
        if self.email is not None:
            return 'User(email={self.email!r})'.format(self=self)
        else:
            return 'User(social={self.social_network!r}, id={self.social_id!r})'.format(self=self)
