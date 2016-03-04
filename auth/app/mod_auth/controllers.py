from flask import Blueprint
from flask import request
from flask import g

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

import json

from app import db
from app.mod_auth.models import User

from app.mod_base.errors import error_response
from app.mod_auth.helpers import create_token
from app.mod_auth.helpers import login_required


auth_module = Blueprint("auth", __name__, url_prefix="/auth")

@auth_module.route("/signup", methods=["POST"])
def signup():

    try:

        params = request.json
        username = params["username"]
        password = params["password"]

        if len(username) == 0 or len(password) == 0:
            return error_response("params_required")

    except Exception as e:
        return error_response("params_required")

    user = User.query.filter_by(mail=username).first()

    if user is None:

        try:

            password = generate_password_hash(password)

            user = User(username, password)
            db.session.add(user)
            db.session.commit()

            response = {"success": True}
            response["id"] = user.id
            response["token"] = create_token(user)
            return json.dumps(response)

        except Exception as e:
            return error_response("user_not_created")

    else:
        return error_response("user_already_exists")


@auth_module.route("/login", methods=["POST"])
def login():

    try:

        params = request.json
        username = params["username"]
        password = params["password"]

        if len(username) == 0 or len(password) == 0:
            return error_response("params_required")

    except Exception as e:
        return error_response("params_required")

    user = User.query.filter_by(mail=username).first()

    if user is not None:

        if check_password_hash(user.password, password):

            response = {"success": True}
            response["id"] = user.id
            response["token"] = create_token(user)
            return json.dumps(response)

        else:
            return error_response("wrong_password")

    else:
        return error_response("user_not_found")


@auth_module.route("/test", methods=["GET"])
@login_required
def authtest():

    return '%s' % g.user.mail

