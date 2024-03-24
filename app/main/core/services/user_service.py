from app.main.model.user_model import User
from app.main.utils.exceptions import NotFoundException
from app.main.core.lib.media_manager import MediaManager


class UserService:

    def __init__(self, media_manager: MediaManager):
        self.media_manager = media_manager

    def get_user_by_id(self, user_id: int):
        user = User.query.filter_by(id=user_id).first()

        if user is None:
            raise NotFoundException("User does not exist")

        return {
            "id": user.id,
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "role": user.role,
            "status": user.status,
            "avatar:": self.media_manager.get_media_url_by_id(user.id),
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat(),
        }
