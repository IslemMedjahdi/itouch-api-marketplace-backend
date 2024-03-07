class MediaService:

    @staticmethod
    def generate_avatar_url(key):
        return f"https://api.dicebear.com/7.x/thumbs/svg?seed={key}&amp;backgroundColor=339AF0&amp;eyes=variant2W10,variant2W12,variant2W14,variant2W16,variant3W10,variant3W12,variant3W14,variant3W16,variant4W10,variant4W12,variant4W14,variant4W16,variant5W10,variant5W12,variant5W14,variant5W16,variant6W10,variant6W12,variant6W14,variant6W16,variant7W10,variant7W12,variant7W14,variant7W16,variant8W10,variant8W12,variant8W14,variant8W16,variant9W10,variant9W12,variant9W14,variant9W16&amp;mouth=variant1,variant2,variant3,variant4"
