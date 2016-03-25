from app import app
from flask import Blueprint
from flask import request
from flask import g
from flask import redirect

from flask.ext.login import LoginManager
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask.ext.login import current_user

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

import json

from app import db
from app.mod_auth.models import User

from app.mod_base.errors import error_response
from app.mod_auth.helpers import create_token
from app.mod_auth.helpers import login_required
from app.mod_auth.utils import gen_random_uuid

from app.mod_auth.user import get_user_by_email


auth_module = Blueprint("auth", __name__, url_prefix="/auth")

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(id):
    user = User.query.get(id)
    return user


@auth_module.route("/signup/", methods=["POST"])
def signup():
    try:
        params = request.json
        email = params["email"]
        password = params["password"]
        if len(email) == 0 or len(password) == 0:
            return error_response("params_required")

    except Exception as e:
        return error_response("params_required")

    user = get_user_by_email(email)

    if user is None:
        try:

            password = generate_password_hash(password)
            id = gen_random_uuid()

            user = User(id=id, email=email, password=password)

            db.session.add(user)
            db.session.commit()

            response = {"success": True}
            response["email"] = user.email
            response["token"] = create_token(user)
            return json.dumps(response)

        except Exception as e:
            print(e)
            return error_response("user_not_created")

    else:
        return error_response("user_already_exists")


@auth_module.route("/login/", methods=["POST"])
def login():

    try:

        params = request.json
        email = params["email"]
        password = params["password"]

        if len(email) == 0 or len(password) == 0:
            return error_response("params_required")

    except Exception as e:
        return error_response("params_required")

    user = get_user_by_email(email)

    if user is not None:

        if check_password_hash(user.password, password):
            login_user(user)
            response = {"success": True}
            response["email"] = user.email
            response["token"] = create_token(user)
            return json.dumps(response)

        else:
            return error_response("wrong_password")

    else:
        return error_response("user_not_found")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')


@auth_module.route("/test", methods=["GET"])
@login_required
def authtest():

    return '%s' % g.user.email

