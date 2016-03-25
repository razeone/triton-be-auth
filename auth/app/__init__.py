from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import flask.ext.login as flask_login

from app.mod_base.access import set_cors
from app.mod_base.access import set_errors


app = Flask(__name__)
app.config.from_object('config')

set_cors(app)
set_errors(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)

from app.mod_auth.controllers import auth_module
app.register_blueprint(auth_module)

db.create_all()

