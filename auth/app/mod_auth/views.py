from flask import Blueprint
from flask import request
from flask import jsonify
from flask.ext.login import LoginManager
from flask.ext.login import login_user
from flask.ext.login import logout_user
from flask.ext.login import login_required
from flask.ext.login import current_user
from werkzeug.security import check_password_hash

from app import app
from app.mod_base.errors import error_response
from app.mod_auth.user import get_user_by_id
from app.mod_auth.user import get_user_by_email
from app.mod_auth.user import get_user_data
from app.mod_auth.user import get_users_data
from app.mod_auth.user import create_user
from app.mod_auth.user import exists_user
from app.mod_auth.user import activate_user
from app.mod_auth.user import recover_password
from app.mod_auth.utils import jwt_required
from app.mod_auth.utils import create_token
from app.mod_auth.utils import send_activate_mail
from app.mod_auth.utils import send_recover_mail
from app.mod_auth.utils import send_profile


auth_module = Blueprint("auth", __name__, url_prefix="/v1/auth")

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    user = get_user_by_id(user_id)
    return user


@auth_module.route("/login", methods=["POST"])
def login_ep():

    try:
        params = request.json
    except Exception as e:
        return error_response("params_required")

    if not 'email' in params:
        return error_response("email_missing")
    if not 'password' in params:
        return error_response("password_missing")

    email = params['email']
    password = params['password']

    user = get_user_by_email(email)

    if user is None:
        return error_response("user_not_found")

    if user.is_active == False:
        return error_response("user_not_active")

    if check_password_hash(user.password, password) == False:
        return error_response("wrong_password")

    login_user(user)

    response = {
        "token": create_token(user)
    }
    return jsonify(response), 200


@auth_module.route("/logout", methods=["POST"])
#@login_required
def logout_ep():

    logout_user()

    response = {}
    return jsonify(response), 200


@auth_module.route("/users", methods=["POST"])
def create_user_ep():

    try:
        params = request.json
    except Exception as e:
        return error_response("params_required")

    if not 'email' in params:
        return error_response("email_missing")
    if not 'password' in params:
        return error_response("password_missing")
    if not 'name' in params:
        return error_response("params_required")
    if not 'lastname' in params:
        return error_response("params_required")

    user_data = {}
    user_data['email'] = params['email']
    user_data['password'] = params['password']
    user_data['name'] = params['name']
    user_data['lastname'] = params['lastname']

    if exists_user(user_data):
        return error_response("user_already_exists")

    user = create_user(user_data)

    if user is None:
        return error_response("user_not_created")

    send_activate_mail(user)
    send_profile(user_data)

    response = {
        "user": user.email
    }
    return jsonify(response), 201


@auth_module.route("/users", methods=["GET"])
#@login_required
def get_users_ep():

    users = get_users_data()

    response = {
        "users": users
    }
    return jsonify(response), 200


@auth_module.route("/users/<user_id>", methods=["GET"])
#@login_required
def get_user_ep(user_id):

    user_instance = get_user_by_id(user_id)
    user = get_user_data(user_instance)

    if user is None:
        return error_response("user_not_found")

    response = {
        "user": user
    }
    return jsonify(response), 200


@auth_module.route("/users/me", methods=["GET"])
@login_required
def get_user_me_ep():

    response = {
        "user_id": current_user.user_id,
        "email": current_user.email
    }
    return jsonify(response), 200


@auth_module.route("/activate/<activate_token>", methods=["GET"])
def activate_ep(activate_token):

    activate = activate_user(activate_token)

    if activate == False:
        return error_response("user_not_found")

    response = {}
    return jsonify(response), 200


@auth_module.route("/recover_request", methods=["POST"])
def recover_password_request_ep():

    try:
        params = request.json
    except Exception as e:
        return error_response("params_required")

    if not 'email' in params:
        return error_response("email_missing")

    email = params['email']

    user = get_user_by_email(email)

    if user is None:
        return error_response("user_not_found")

    if user.is_active == False:
        return error_response("user_not_active")

    send_recover_mail(user)

    response = {}
    return jsonify(response), 200


@auth_module.route("/recover_password", methods=["POST"])
def recover_password_ep():

    try:
        params = request.json
    except Exception as e:
        return error_response("params_required")

    recover_token = params['token']
    password = params['password']

    recover = recover_password(recover_token, password)

    if recover == False:
        return error_response("user_not_found")

    response = {}
    return jsonify(response), 200
