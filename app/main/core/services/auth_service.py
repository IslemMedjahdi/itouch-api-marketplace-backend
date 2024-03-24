from typing import Dict
from app.main.model.user_model import User
from app.main import db
from app.main.utils.exceptions import NotFoundException, BadRequestException
from app.main.utils.validators import is_email_valid


class AuthService:

    def login(self, data: Dict):
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if user is None:
            raise NotFoundException("User does not exist")

        if not user.check_password(password):
            raise BadRequestException("email or password does not match.")

        if not user.check_status("active"):
            raise BadRequestException("User is not active.")

        auth_token = User.encode_auth_token(user.id)

        return auth_token

    def register(self, data: Dict):
        email = data.get("email", "")
        password = data.get("password", "")
        firstname = data.get("firstname", "")
        lastname = data.get("lastname", "")

        user = User.query.filter_by(email=email).first()
        if user:
            raise BadRequestException("User already exists. Please Log in.")

        if not is_email_valid(email):
            raise BadRequestException("Invalid email format")

        new_user = User(
            email=email, password=password, firstname=firstname, lastname=lastname
        )

        db.session.add(new_user)
        db.session.commit()
