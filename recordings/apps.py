from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RecordingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recordings'
    verbose_name = _('Recordings')
