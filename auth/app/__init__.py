import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.mod_base.access import configure_access


buildmode = os.environ['APP_SETTINGS']

app = Flask(__name__)
app.config.from_object(buildmode)
print("Loading configuraton from: " + buildmode)

configure_access(app)
db = SQLAlchemy(app)

from app.mod_auth.views import auth_module
app.register_blueprint(auth_module)

db.create_all()
