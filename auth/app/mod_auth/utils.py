import json
import jwt
import random
from functools import wraps
from datetime import datetime
from datetime import timedelta

from flask import request
from flask import g
from jwt import DecodeError
from jwt import ExpiredSignature

from app import app
from app.mod_base.errors import error_response
from app.mod_base.utils import send_message
from app.mod_auth.user import get_user_by_email
from app.mod_auth.user import save_user


secretKey = app.config['SECRET_KEY']
encryption = app.config['ENCRYPTION_ALGORITHM']


def create_token(user):

    payload = {
        "sub": user.email,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(days=1)
    }

    token = jwt.encode(payload, secretKey, algorithm=encryption)
    return token.decode('unicode_escape')


def parse_token(req):

    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, secretKey, algorithms=encryption)


def jwt_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not request.headers.get('Authorization'):
            return error_response("token_required")

        try:
            payload = parse_token(request)

            email = payload['sub']
            user = get_user_by_email(email)

            if user is None:
                return error_response("user_not_found")

            g.user = user

        except DecodeError:
            return error_response("token_invalid")
        except ExpiredSignature:
            return error_response("token_expired")

        return f(*args, **kwargs)

    return decorated_function


def send_activate_mail(user):

    mail = user.email
    token = user.activation_token
    message = json.dumps({"mail": mail, "token": token})
    send_message("activate", message)


def send_recover_mail(user):

    token = str(random.getrandbits(128))
    user.activation_token = token
    save_user(user)

    mail = user.email
    message = json.dumps({"mail": mail, "token": token})
    send_message("recover", message)


def send_profile(user):

    name = user['name']
    lastname = user['lastname']
    mail = user['email']

    message = json.dumps({"name": name, "lastname": lastname, "user": mail})
    send_message("profile", message)
