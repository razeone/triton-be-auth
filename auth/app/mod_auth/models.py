from app import db

class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key = True)
    created = db.Column(db.DateTime, default = db.func.current_timestamp())
    modified = db.Column(db.DateTime, default = db.func.current_timestamp(), onupdate = db.func.current_timestamp())


class User(Base):

    __tablename__ = 'user'

    mail = db.Column(db.String(128), unique = True, nullable = False)
    password = db.Column(db.String(192), nullable = False)

    def __init__(self, mail, password):
        self.mail = mail
        self.password = password

    def __repr__(self):
        return "<User %r>" % (self.mail)


class Profile(Base):

    __tablename__ = 'profile'



    user = db.Column(db.Integer, db.ForeignKey("user.id"))

