from app import db
from app.mod_base.models import Base


class User(Base):

    __tablename__ = 'user'

    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(192), nullable=False)
    #active = db.Column(db.Boolean(), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password
        #self.active = False

