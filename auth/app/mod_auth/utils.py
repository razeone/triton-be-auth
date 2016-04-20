import uuid
import jwt
import redis
import json

from app import app
from flask import request
from flask import g

from jwt import DecodeError
from jwt import ExpiredSignature

from functools import wraps
from datetime import datetime
from datetime import timedelta

from app.mod_auth.models import User
from app.mod_base.errors import error_response


redisClient = redis.StrictRedis(app.config['REDIS_HOST'], app.config['REDIS_PORT'])


def create_token(user):

    payload = {
        "sub": user.email,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(days=1)
    }

    token = jwt.encode(
        payload,
        app.config['SECRET_KEY'],
        algorithm=app.config['ENCRYPTION_ALGORITHM']
        )
    return token.decode('unicode_escape')


def parse_token(req):

    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(
        token,
        app.config['SECRET_KEY'],
        algorithms=app.config['ENCRYPTION_ALGORITHM']
        )


def jwt_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not request.headers.get('Authorization'):
            return error_response("token_required")

        try:

            payload = parse_token(request)

            email = payload['sub']
            user = User.query.filter_by(email=email).first()

            if user is None:
                return error_response("user_not_found")

        except DecodeError:
            return error_response("token_invalid")

        except ExpiredSignature:
            return error_response("token_expired")

        g.user = user

        return f(*args, **kwargs)

    return decorated_function


def gen_random_uuid():
    return uuid.uuid4()


def send_activate_mail(user):

    mail = user.email
    token = user.activation_token
    message = json.dumps({"mail": mail, "token": token})

    redisClient.publish("activate", message)


def send_recover_mail(user):

    mail = user.email
    token = gen_random_uuid()
    message = json.dumps({"mail": mail, "token": token})

    redisClient.set(token, user.user_id)
    redisClient.publish("recover", message)

def get_recover_id(recover_token):
    user_id = redisClient.get(recover_token)
    return user_id

