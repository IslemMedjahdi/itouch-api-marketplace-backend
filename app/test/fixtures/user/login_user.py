from app.main.model.user_model import User


def login_user(user_id):
    auth_token = User.encode_auth_token(user_id)

    return auth_token
