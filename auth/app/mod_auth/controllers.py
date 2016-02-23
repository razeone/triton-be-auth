from flask import Blueprint, request, render_template
import json

from app import db
from app.mod_auth.models import User

auth_module = Blueprint("auth", __name__, url_prefix="/auth")

@auth_module.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "GET":
        return render_template("signup.html")

    else:

        mail = request.form["mail"]
        password = request.form["password"]

        if len(mail) > 0 and len(password) > 0:

            try:
                user = User(mail, password)
                db.session.add(user)
                db.session.commit()

                response = {"success": True}
                response["id"] = user.id
                response["token"] = "" # generate token

                return json.dumps(response)

            except: # exc.SQLAlchemyError:

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

                if user.password == password:

                    response = {"success": True}
                    response["id"] = user.id

                    return json.dumps(response)

                else:

                    response = {"success": False}
                    response["error"] = "wrong password"

                    return json.dumps(response)

        else:

            response = {"success": False}
            response["error"] = "mail and password required"

            return json.dumps(response)

