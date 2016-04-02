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

from app.mod_auth.user import get_user_by_email
from app.mod_auth.user import create_user
from app.mod_auth.user import get_users
from app.mod_auth.user import get_user


auth_module = Blueprint("auth", __name__, url_prefix="/v1/auth")

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(id):
    user = User.query.get(id)
    return user


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
            return jsonify(response)

        else:
            return error_response("wrong_password")

    else:
        return error_response("user_not_found")


@auth_module.route("/logout")
@login_required
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


@auth_module.route("/users/", methods=["GET", "POST"])
def users():
    if request.method == "POST":
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
                response = create_user(email, password)
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


@auth_module.route("/users/<user_id>")
def get_user_dettail(user_id):
    try:
        response = get_user(user_id)
    except Exception as e:
        return error_response("user_not_found")
    if response[0]:
        return jsonify(response[1].data), 200
    else:
        return error_response("user_not_found")


@auth_module.route("/test", methods=["GET"])
@login_required
def authtest():
    return '%s' % user_loader(current_user.email)
