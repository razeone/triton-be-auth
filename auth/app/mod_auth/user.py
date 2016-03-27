from app.mod_auth.models import User
from werkzeug.security import generate_password_hash
from app.mod_auth.helpers import create_token
from app.mod_auth.utils import gen_random_uuid

from app import db


def create_user(email, password):
    password = generate_password_hash(password)
    id = gen_random_uuid()

    user = User(id=id, email=email, password=password)

    db.session.add(user)
    db.session.commit()

    response = {"success": True}
    response["id"] = user.id
    response["email"] = user.email
    return response


def get_user(id):
    user_instance = User.query.get(id)
    return user_instance


def get_user_by_email(email):
    user_instance = User.query.filter_by(email=email).first()
    return user_instance
