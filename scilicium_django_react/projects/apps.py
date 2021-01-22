from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProjectsConfig(AppConfig):
    name = "scilicium_django_react.projects"
    verbose_name = _("Projects")
