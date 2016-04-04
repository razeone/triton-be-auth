from app.mod_auth.models import User
from werkzeug.security import generate_password_hash
from app.mod_auth.utils import gen_random_uuid
from app.mod_auth.user_schema import UserSchema

from app import db


def create_user(email, password):
    try:
        password = generate_password_hash(password)
        id = gen_random_uuid()

        user = User(id=id, email=email, password=password)

        db.session.add(user)
        db.session.commit()

        response = {"success": True}
        response["id"] = user.id
        response["email"] = user.email
        return response
    except Exception as e:
        return False, {"error": "Error creating user " + str(e)}


def get_user(id):
    try:
        user_instance = User.query.get(id)
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
