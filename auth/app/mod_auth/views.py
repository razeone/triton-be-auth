from app import app

from flask import Blueprint
from flask import request
from flask import jsonify

from flask.ext.login import LoginManager
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask.ext.login import login_required
from flask.ext.login import current_user

from werkzeug.security import check_password_hash

from app.mod_auth.models import User

from app.mod_base.errors import error_response

from app.mod_auth.utils import create_token
from app.mod_auth.utils import jwt_required
from app.mod_auth.utils import send_recover_mail

from app.mod_auth.user import get_user_by_email
from app.mod_auth.user import create_user
from app.mod_auth.user import get_users
from app.mod_auth.user import get_user
from app.mod_auth.user import activate_user
from app.mod_auth.user import recover_password


auth_module = Blueprint("auth", __name__, url_prefix="/v1/auth")

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    user = User.query.get(user_id)
    return user


@auth_module.route("/login", methods=["POST"])
def login():
    try:
        params = request.json
    except Exception as e:
        return error_response("params_required")
    if not 'email' in params:
        return error_response("email_missing")
    if not 'password' in params:
        return error_response("password_missing")

    email = params["email"]
    password = params["password"]

    if len(email) == 0 or len(password) == 0:
        return error_response("params_required")

    user = get_user_by_email(email)

    if user is not None:
        if check_password_hash(user.password, password):
            if user.is_active == True:
                login_user(user)
                response = {"success": True}
                response["email"] = user.email
                response["token"] = create_token(user)
                return jsonify(response)
            else:
                return error_response("user_not_active")
        else:
            return error_response("wrong_password")
    else:
        return error_response("user_not_found")


@auth_module.route("/logout", methods=["POST"])
@jwt_required
def logout():
    try:
        logout_user()
        response = {
            "success": True,
            "message": "Success logout"
        }
        return jsonify(response), 200
    except Exception as e:
        return error_response(e)


@auth_module.route("/activate/<activate_token>", methods=["GET"])
def activate(activate_token):
    try:
        response = activate_user(activate_token)

        if response[0]:
            return jsonify(response[1]), 200
        else:
            return error_response("user_not_found")
    except Exception as e:
        return error_response(e)


@auth_module.route("/recover_request", methods=["POST"])
def recover_request():

    try:
        params = request.json
    except Exception as e:
        return error_response("params_required")
    if not 'email' in params:
        return error_response("email_missing")

    email = params["email"]

    user = get_user_by_email(email)

    if user is not None:
        if user.is_active == True:

            recover_password(user)

            response = {"success": True}
            return jsonify(response)

        else:
            return error_response("user_not_active")
    else:
        return error_response("user_not_found")


@auth_module.route("/recover", methods=["POST"])
def recover():

    try:
        params = request.json
    except Exception as e:
        return error_response("params_required")

    recover_token = params["token"]
    password = params["password"]

    response = recover_password(recover_token, password)

    if response[0]:
        return jsonify(response[1].data), 200
    else:
        return error_response("user_not_found")


@auth_module.route("/users", methods=["GET", "POST"])
def users():

    if request.method == "POST":
        try:
            params = request.json
        except Exception as e:
            return error_response("params_required")

        if not 'email' in params:
            return error_response("email_missing")
        if not 'password' in params:
            return error_response("password_missing")
        if len(params["email"]) == 0 or len(params["password"]) == 0:
            return error_response("params_required")

        user_data = {}
        user_data["email"] = params["email"]
        user_data["password"] = params["password"]

        user = get_user_by_email(user_data["email"])

        if user is None:
            try:
                response = create_user(user_data)
                return jsonify(response), 201

            except Exception as e:
                return error_response("user_not_created")
        else:
            return error_response("user_already_exists")
    if request.method == "GET":
        try:
            response = get_users()
            return jsonify({"users": response.data})
        except Exception as e:
            return error_response("user_not_found")


@auth_module.route("/users/<user_id>", methods=["GET"])
@login_required
def get_user_dettail(user_id):
    try:
        response = get_user(user_id)
    except Exception as e:
        return error_response("user_not_found")
    if response[0]:
        return jsonify(response[1].data), 200
    else:
        return error_response("user_not_found")


@auth_module.route("/users/me", methods=["GET"])
@login_required
def authtest():
    response = {
        "user_id": current_user.user_id,
        "email": current_user.email
    }
    return jsonify(response), 200

