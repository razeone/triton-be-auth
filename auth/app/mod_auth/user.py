import random
from app import db

from app.mod_auth.models import User
from werkzeug.security import generate_password_hash
from app.mod_auth.utils import gen_random_uuid
from app.mod_auth.user_schema import UserSchema


def create_user(user_data):
    try:
        password = generate_password_hash(user_data["password"])
        user_id = gen_random_uuid()
        activation_token = str(random.getrandbits(128))

        user = User(
            user_id=user_id,
            email=user_data["email"],
            password=password,
            activation_token=activation_token
            )

        db.session.add(user)
        db.session.commit()

        response = {"success": True}
        response["user_id"] = user.user_id
        response["email"] = user.email
        return response
    except Exception as e:
        print(e)
        return False, {"error": "Error creating user"}


def get_user(user_id):
    try:
        user_instance = User.query.get(user_id)
        user_schema = UserSchema()
        result = user_schema.dump(user_instance)
        return True, result
    except Exception as e:
        return False, {"error": "User not found"}


def get_user_by_email(email):
    user_instance = User.query.filter_by(email=email).first()
    return user_instance


def get_users():
    users = User.query.all()
    users_schema = UserSchema(many=True)
    result = users_schema.dump(users)
    return result
