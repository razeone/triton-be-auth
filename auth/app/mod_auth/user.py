import uuid
import random
from datetime import datetime

from werkzeug.security import generate_password_hash

from app import db
from app.mod_auth.models import User
from app.mod_auth.schemas import UserSchema


def create_user(user_data):

    try:
        user_id = uuid.uuid4()
        email = user_data['email']
        password = generate_password_hash(user_data["password"])
        activation_token = str(random.getrandbits(128))

        user = User(
            user_id=user_id,
            email=email,
            password=password,
            activation_token=activation_token
            )

        db.session.add(user)
        db.session.commit()

        return user

    except Exception as e:
        return None


def create_social_user(user_data):

    try:
        user_id = uuid.uuid4()
        social_id = user_data['social_id']
        social_network = user_data['social_network']
        email = user_data['email']

        user = User(
            user_id=user_id,
            social_id=social_id,
            social_network=social_network,
            email=email
            )

        db.session.add(user)
        db.session.commit()

        return user

    except Exception as e:
        return None


def save_user(user):
    db.session.add(user)
    db.session.commit()


def get_user_by_id(id):

    try:
        user_id = uuid.UUID(id).hex
    except Exception as e:
        return None

    user_instance = User.query.get(user_id)
    return user_instance


def get_user_by_email(email):

    user_instance = User.query.filter_by(email=email).first()
    return user_instance


def get_user_by_social_id(social_id, social_network):

    user_instance = User.query.filter_by(social_id=social_id, social_network=social_network).first()
    return user_instance


def get_user_by_token(token):

    user_instance = User.query.filter_by(activation_token=token).first()
    return user_instance


def get_user_data(user_instance):

    if user_instance is None:
        return None

    try:
        user_schema = UserSchema()
        result = user_schema.dump(user_instance)
        return result.data
    except Exception as e:
        return None


def get_users_data():
    users = User.query.all()
    users_schema = UserSchema(many=True)
    result = users_schema.dump(users)
    return result.data


def exists_user(user_data):

    email = user_data['email']
    user = get_user_by_email(email)
    return user is not None


def activate_user(activation_token):

    user = get_user_by_token(activation_token)

    if user is None:
        return False

    user.is_active = True
    user.activation_token = None
    user.confirmated_at = datetime.utcnow()
    save_user(user)

    return True


def recover_password(recover_token, new_password):

    user = get_user_by_token(recover_token)

    if user is None:
        return False

    user.password = generate_password_hash(new_password)
    user.activation_token = None
    save_user(user)

    return True
