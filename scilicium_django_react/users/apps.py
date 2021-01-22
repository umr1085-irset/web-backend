from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "scilicium_django_react.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import scilicium_django_react.users.signals  # noqa F401
        except ImportError:
            pass
