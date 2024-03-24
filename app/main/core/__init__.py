from app.main.core.lib.media_manager import MediaManager
from app.main.core.lib.rest_client import RestClient
from app.main.core.lib.chargily_api import ChargilyApi


class ServicesInitializer:
    @staticmethod
    def an_auth_service():
        from app.main.core.services.auth_service import AuthService

        return AuthService()

    @staticmethod
    def a_user_service():
        from app.main.core.services.user_service import UserService

        return UserService(media_manager=MediaManager())

    @staticmethod
    def an_api_service():
        from app.main.core.services.api_service import ApiService

        return ApiService(
            media_manager=MediaManager(), chargily_api=ChargilyApi(RestClient())
        )

    @staticmethod
    def an_api_category_service():
        from app.main.core.services.api_category_service import ApiCategoryService

        return ApiCategoryService()

    @staticmethod
    def an_api_version_service():
        from app.main.core.services.api_version_service import ApiVersionService

        return ApiVersionService()

    @staticmethod
    def an_api_tests_service():
        from app.main.core.services.api_tests_service import ApiTestsService

        return ApiTestsService(rest_client=RestClient())

    @staticmethod
    def a_discussion_service():
        from app.main.core.services.api_discussion_service import ApiDiscussionService

        return ApiDiscussionService()
