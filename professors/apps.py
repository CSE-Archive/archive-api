from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProfessorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'professors'
    verbose_name = _('Professors')

    def ready(self):
        import professors.signals

