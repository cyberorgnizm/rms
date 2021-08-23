from django.apps import AppConfig


class RestaurantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rms.apps.restaurants'

    # disable post migration signals
    # def ready(self) -> None:
    #     from . import signals