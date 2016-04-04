from app import db
from sqlalchemy_utils import UUIDType
from flask.ext.login import UserMixin
import datetime


class User(UserMixin, db.Model):

    __tablename__ = 'user'

    id = db.Column(UUIDType, unique=True, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    password = db.Column(db.String(192), nullable=False)

    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User(email={self.email!r})'.format(self=self)
