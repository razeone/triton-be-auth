import requests
import json
from urllib.parse import parse_qsl
from requests_oauthlib import OAuth1

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
from app.mod_auth.user import get_user_by_social_id
from app.mod_auth.user import get_user_data
from app.mod_auth.user import get_users_data
from app.mod_auth.user import create_user
from app.mod_auth.user import create_social_user
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
    user_data['user'] = params['email']

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
@jwt_required
def get_users_ep():

    users = get_users_data()

    response = {
        "users": users
    }
    return jsonify(response), 200


@auth_module.route("/users/<user_id>", methods=["GET"])
@login_required
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


@auth_module.route("/facebook", methods=["POST"])
def login_facebook_ep():

    try:
        params = request.json
    except Exception as e:
        return error_response("params_required")

    access_token_url = 'https://graph.facebook.com/v2.6/oauth/access_token'
    graph_api_url = 'https://graph.facebook.com/v2.6/me?fields=id,first_name,last_name,email'

    social_network = "facebook"
    clientId = params['clientId']
    clientSecret = app.config['FACEBOOK_SECRET']
    redirectUri = params['redirectUri']
    code = params['code']

    params = {
        "client_id": clientId,
        "client_secret": clientSecret,
        "redirect_uri": redirectUri,
        "code": code
    }

    r = requests.get(access_token_url, params)
    access_token = json.loads(r.text)

    r = requests.get(graph_api_url, access_token)
    profile = json.loads(r.text)

    social_id = profile['id']

    email = ""
    if 'email' in profile:
        email = profile['email']

    name = profile['first_name']
    lastname = profile['last_name']

    return login_social_ep(social_id, social_network, email, name, lastname)


@auth_module.route("/twitter", methods=["POST"])
def login_twitter_ep():

    try:
        params = request.json
    except Exception as e:
        return error_response("params_required")

    request_token_url = 'https://api.twitter.com/oauth/request_token'
    access_token_url = 'https://api.twitter.com/oauth/access_token'

    social_network = "twitter"
    clientId = app.config['TWITTER_KEY']
    clientSecret = app.config['TWITTER_SECRET']

    if params.get('oauth_token') and params.get('oauth_verifier'):

        oauthToken = params['oauth_token']
        oauthVerifier = params['oauth_verifier']
        auth = OAuth1(
            clientId,
            client_secret=clientSecret,
            resource_owner_key=oauthToken,
            verifier=oauthVerifier
            )

        r = requests.post(access_token_url, auth=auth)
        profile = dict(parse_qsl(r.text))

        social_id = profile['user_id']

        email = ""
        if 'email' in profile:
            email = profile['email']

        name = profile['screen_name']
        lastname = ""

        return login_social_ep(social_id, social_network, email, name, lastname)

    else:

        redirectUri = params['redirectUri']
        auth = OAuth1(
            clientId,
            client_secret=clientSecret,
            callback_uri=redirectUri
            )

        r = requests.post(request_token_url, auth=auth)
        oauth_token = dict(parse_qsl(r.text))

        return jsonify(oauth_token)


@auth_module.route("/google", methods=["POST"])
def login_google_ep():

    try:
        params = request.json
    except Exception as e:
        return error_response("params_required")

    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    people_api_url = 'https://www.googleapis.com/plus/v1/people/me/openIdConnect'

    social_network = "google"
    clientId = params['clientId']
    clientSecret = app.config['GOOGLE_SECRET']
    redirectUri = params['redirectUri']
    code = params['code']

    params = dict(
        client_id=clientId,
        client_secret=clientSecret,
        redirect_uri=redirectUri,
        code=code,
        grant_type='authorization_code'
        )

    r = requests.post(access_token_url, data=params)
    access_token = json.loads(r.text)
    token = access_token['access_token']
    headers = {'Authorization': 'Bearer {0}'.format(token)}

    r = requests.get(people_api_url, headers=headers)
    profile = json.loads(r.text)

    social_id = profile['sub']

    email = ""
    if 'email' in profile:
        email = profile['email']

    name = profile['given_name']
    lastname = profile['family_name']

    return login_social_ep(social_id, social_network, email, name, lastname)


@auth_module.route("/github", methods=["POST"])
def login_github_ep():

    try:
        params = request.json
    except Exception as e:
        return error_response("params_required")

    access_token_url = 'https://github.com/login/oauth/access_token'
    users_api_url = 'https://api.github.com/user'

    social_network = "github"
    clientId = params['clientId']
    clientSecret = app.config['GITHUB_SECRET']
    code = params['code']
    redirectUri = params['redirectUri']

    params = {
        "client_id": clientId,
        "client_secret": clientSecret,
        "redirect_uri": redirectUri,
        "code": code
    }

    r = requests.get(access_token_url, params)
    access_token = dict(parse_qsl(r.text))

    r = requests.get(users_api_url, access_token)
    profile = json.loads(r.text)

    social_id = profile['id']

    email = ""
    if 'email' in profile:
        email = profile['email']

    name = profile['name']
    lastname = ""

    return login_social_ep(social_id, social_network, email, name, lastname)


def login_social_ep(social_id, social_network, email, name, lastname):

    user_data = {}
    user_data['social_id'] = social_id
    user_data['social_network'] = social_network
    user_data['email'] = email
    user_data['name'] = name
    user_data['lastname'] = lastname
    user_data['user'] = social_network + ":" + str(social_id)

    user = get_user_by_social_id(social_id, social_network)

    if user is None:
        user = create_social_user(user_data)

        if user is None:
            return error_response("user_not_created")

        send_profile(user_data)

    login_user(user)

    response = {
        "token": create_token(user)
    }
    return jsonify(response), 200
