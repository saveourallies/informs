from django.apps import AppConfig

# from icecream import ic


class AidRequestsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aidrequests'

    def ready(self):
        import aidrequests.signals  # noqa: F401
