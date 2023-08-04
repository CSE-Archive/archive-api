from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ClassroomsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'classrooms'
    verbose_name = _('Classrooms')
