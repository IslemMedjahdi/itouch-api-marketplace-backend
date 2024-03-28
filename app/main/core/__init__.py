from app.main.core.lib.impl.media_manager_impl import MediaManagerImpl
from app.main.core.lib.impl.rest_client_impl import RestClientImpl
from app.main.core.lib.chargily_api import ChargilyApi


class ServicesInitializer:
    @staticmethod
    def an_auth_service():
        from app.main.core.services.auth_service import AuthService

        return AuthService()

    @staticmethod
    def a_user_service():
        from app.main.core.services.user_service import UserService

        return UserService(media_manager=MediaManagerImpl())

    @staticmethod
    def an_api_service():
        from app.main.core.services.api_service import ApiService

        return ApiService(
            media_manager=MediaManagerImpl(), chargily_api=ChargilyApi(RestClientImpl())
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

        return ApiTestsService(rest_client=RestClientImpl())

    @staticmethod
    def a_discussion_service():
        from app.main.core.services.api_discussion_service import ApiDiscussionService

        return ApiDiscussionService()

    @staticmethod
    def an_api_subscription_service():
        from app.main.core.services.api_subscription_service import (
            ApiSubscriptionService,
        )

        return ApiSubscriptionService(chargily_api=ChargilyApi(RestClientImpl()))
