from django.urls import path
from django.conf import settings
from django.views.decorators.cache import cache_page

from chart.views import ChartView


urlpatterns = [
    path("chart/", cache_page(settings.CHART_VIEW_CACHE_TIMEOUT)(ChartView.as_view()), name="chart"),
]
