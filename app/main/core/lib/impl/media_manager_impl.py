from app.main.core.lib.media_manager import MediaManager


class MediaManagerImpl(MediaManager):
    def get_media_url_by_id(self, media_id) -> str:
        raise Exception("You must implement this method in a subclass.")
