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
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response

        try:
            payload = parse_token(request)
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
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

        mail = request.form["mail"]
        password = request.form["password"]

        if len(mail) > 0 and len(password) > 0:

            password = generate_password_hash(password)

            try:
                user = User(mail, password)
                db.session.add(user)
                db.session.commit()

                response = {"success": True}
                response["id"] = user.id
                response["token"] = create_token(user)

                return json.dumps(response)

            except Exception as e: # exc.SQLAlchemyError:

                print(e)

                response = {"success": False}
                response["error"] = "user already exists"

                return json.dumps(response)
        
        else:

            response = {"success": False}
            response["error"] = "mail and password required"

            return json.dumps(response)


@auth_module.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    else:

        mail = request.form["mail"]
        password = request.form["password"]

        if len(mail) > 0 and len(password) > 0:

            user = User.query.filter_by(mail=mail).first()

            if user is None:

                response = {"success": False}
                response["error"] = "user not found"

                return json.dumps(response)

            else:

                if check_password_hash(user.password, password):

                    response = {"success": True}
                    response["id"] = user.id
                    response["token"] = create_token(user)

                    return json.dumps(response)

                else:

                    response = {"success": False}
                    response["error"] = "wrong password"

                    return json.dumps(response)

        else:

            response = {"success": False}
            response["error"] = "mail and password required"

            return json.dumps(response)


@auth_module.route("/test", methods=["GET"])
@login_required
def authtest():

    return '%d' % g.user_id

