from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images'

    def ready(self):
        # Import procedur obsługi sygnałów
        import images.signals
