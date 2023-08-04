from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(title="CSE Archive", default_version="v1"),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

admin.site.site_title = "CSE Archive"
admin.site.index_title = _("Admin Panel")
admin.site.site_header = _("CSE Archive Admin Panel")

urlpatterns = [
    path("", include("courses.urls")),
    path("", include("classrooms.urls")),
    path("", include("professors.urls")),
    path("", include("references.urls")),
    path("", include("resources.urls")),
    path("", include("recordings.urls")),
    path("", include("chart.urls")),
    path("", include("core.urls")),

    path("i18n/", include("django.conf.urls.i18n")),
] + i18n_patterns(
    path("admin/", admin.site.urls),
)

if settings.DEBUG:
    debug_urlpatterns = [
        path("__debug__/", include("debug_toolbar.urls")),
        path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.extend(debug_urlpatterns)
