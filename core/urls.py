from django.urls import path
from django.views.generic import TemplateView

from core.views import HomeView, SearchView


urlpatterns = [
    path("", TemplateView.as_view(template_name="core/index.html")),
    path("home/", HomeView.as_view(), name="home"),
    path("search/", SearchView.as_view(), name="search"),
]
