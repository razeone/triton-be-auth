from flask import Blueprint, request, jsonify, render_template, g
from werkzeug.security import generate_password_hash, check_password_hash
from jwt import DecodeError, ExpiredSignature
from functools import wraps
from datetime import datetime, timedelta
from config import SECRET_KEY
import jwt, json, datetime

from app import app
from app import db
from app.mod_auth.models import User


def create_token(user):

    payload = {
        "sub": user.id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + timedelta(days=1)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token.decode('unicode_escape')


def parse_token(req):

    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, SECRET_KEY, algorithms='HS256')


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not request.headers.get('Authorization'):

            response = jsonify(success=False, error="token is required")
            response.status_code = 401
            return response

        try:

            payload = parse_token(request)

        except DecodeError:

            response = jsonify(success=False, error="token is invalid")
            response.status_code = 401
            return response

        except ExpiredSignature:

            response = jsonify(success=False, error="token has expired")
            response.status_code = 401
            return response

        g.user_id = payload['sub']

        return f(*args, **kwargs)

    return decorated_function



auth_module = Blueprint("auth", __name__, url_prefix="/auth")

@auth_module.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "GET":
        return render_template("signup.html")

    else:

        try:

            params = request.json
            username = params["username"]
            password = params["password"]

        except Exception as e:
            print(e)
            response = jsonify(success=False, error="params not available")
            return response


        if len(username) > 0 and len(password) > 0:

            password = generate_password_hash(password)

            try:

                user = User(username, password)
                db.session.add(user)
                db.session.commit()

                response = {"success": True}
                response["id"] = user.id
                response["token"] = create_token(user)
                return json.dumps(response)

            except Exception as e:
                print(e)
                response = jsonify(success=False, error="user already exists")
                return response
        
        else:
            response = jsonify(success=False, error="params not available")
            return response


@auth_module.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    else:

        try:

            params = request.json
            username = params["username"]
            password = params["password"]

        except Exception as e:
            print(e)
            response = jsonify(success=False, error="params not available")
            return response


        if len(username) > 0 and len(password) > 0:

            user = User.query.filter_by(mail=username).first()

            if user is not None:

                if check_password_hash(user.password, password):

                    response = {"success": True}
                    response["id"] = user.id
                    response["token"] = create_token(user)
                    return json.dumps(response)

                else:
                    response = jsonify(success=False, error="wrong password")
                    return response

            else:
                response = jsonify(success=False, error="user not found")
                return response

        else:
            response = jsonify(success=False, error="params not available")
            return response


@auth_module.route("/test", methods=["GET"])
@login_required
def authtest():

    return '%d' % g.user_id

