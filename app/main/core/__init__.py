from app.main.core.lib.media_manager import MediaManager


class ServicesInitializer:
    @staticmethod
    def an_api_service():
        from app.main.core.services.api_service import ApiService

        return ApiService(media_manager=MediaManager())

    @staticmethod
    def an_api_category_service():
        from app.main.core.services.api_category_service import ApiCategoryService

        return ApiCategoryService()
