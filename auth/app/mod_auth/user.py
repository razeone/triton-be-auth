from app.mod_auth.models import User


def get_user_by_email(email):
    user_instance = User.query.filter_by(email=email).first()
    return user_instance
