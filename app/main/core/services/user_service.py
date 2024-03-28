from app.main.model.user_model import User
from app.main.utils.exceptions import NotFoundError, BadRequestError
from app.main.core.lib.media_manager import MediaManager
from app.main import db
from app.main.utils.validators import is_email_valid
from app.main.utils.roles import Role
from typing import Dict


class UserService:

    def __init__(self, media_manager: MediaManager):
        self.media_manager = media_manager

    def get_user_by_id(self, user_id: int):
        user = User.query.filter_by(id=user_id).first()

        if user is None:
            raise NotFoundError("User does not exist")

        return {
            "id": user.id,
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "role": user.role,
            "status": user.status,
            "avatar:": self.media_manager.get_media_url_by_id(
                user.id
            ),  # TODO: this will be user.avatar_id
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat(),
            "phone_number": user.phone_number,
            "bio": user.bio,
        }

    def get_users(self, query_params: Dict):
        page = query_params.get("page", 1)
        per_page = query_params.get("per_page", 10)
        status = query_params.get("status", None)
        roles = query_params.get("role", None)

        query = User.query

        if status:
            query = query.filter_by(status=status)

        if roles:
            query = query.filter(User.role.in_(roles))

        users = query.paginate(page=page, per_page=per_page)

        return (
            [
                {
                    "id": user.id,
                    "email": user.email,
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                    "role": user.role,
                    "status": user.status,
                    "avatar:": self.media_manager.get_media_url_by_id(user.id),
                    "created_at": user.created_at.isoformat(),
                    "updated_at": user.updated_at.isoformat(),
                    "phone_number": user.phone_number,
                    "bio": user.bio,
                }
                for user in users.items
            ],
            {
                "page": users.page,
                "per_page": users.per_page,
                "pages": users.pages,
                "total": users.total,
            },
        )

    def activate_user(self, user_id: int):
        user = User.query.filter_by(id=user_id).first()

        if user is None:
            raise NotFoundError("User does not exist")

        user.status = "active"
        # user.save()
        db.session.commit()

    def suspend_user(self, user_id: int):
        user = User.query.filter_by(id=user_id).first()

        if user is None:
            raise NotFoundError("User does not exist")

        user.status = "suspended"
        # user.save()
        db.session.commit()

    def create_supplier(self, data: Dict):
        email = data.get("email", "")
        password = data.get("password", "")
        firstname = data.get("firstname", "")
        lastname = data.get("lastname", "")

        user = User.query.filter_by(email=email).first()
        if user:
            raise BadRequestError("User already exists. Please Log in.")

        if not is_email_valid(email):
            raise BadRequestError("Invalid email format")

        new_user = User(
            email=email,
            password=password,
            firstname=firstname,
            lastname=lastname,
            role=Role.SUPPLIER,
        )

        db.session.add(new_user)
        db.session.commit()

    def edit_user(self, user_id: int, data: Dict):
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            raise NotFoundError("User does not exist")

        user.firstname = data.get("firstname", user.firstname)
        user.lastname = data.get("lastname", user.lastname)
        user.bio = data.get("bio", user.bio)
        user.phone_number = data.get("phone_number", user.phone_number)

        db.session.commit()
