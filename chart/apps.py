from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ChartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chart'
    verbose_name = _('Chart')
