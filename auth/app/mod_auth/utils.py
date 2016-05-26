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
from app.mod_auth.user import get_user_by_social_id
from app.mod_auth.user import save_user


secretKey = app.config['SECRET_KEY']
encryption = app.config['ENCRYPTION_ALGORITHM']


def create_token(user):

    if user.social_network is None:
        id = user.email
        network = "email"
    else:
        id = user.social_id
        network = user.social_network

    payload = {
        "sub": id,
        "iss": network,
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

            id = payload['sub']
            network = payload['iss']

            if network == "email":
                user = get_user_by_email(email)
            else:
                user = get_user_by_social_id(id, network)

            if user is None:
                return error_response("user_not_found")

            g.user = user

        except DecodeError as de:
            return error_response("token_invalid")
        except ExpiredSignature as es:
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
    email = user['email']
    user = user['user']

    message = json.dumps({"name": name, "lastname": lastname, "email": email, "user": user})
    send_message("profile", message)
