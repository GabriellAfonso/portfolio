from django.apps import AppConfig


class ContentConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "apps.content"
