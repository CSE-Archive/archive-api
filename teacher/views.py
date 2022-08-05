from .models import Teacher
from .serializers import TeacherSerializer
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend


class TeacherViewSet(ReadOnlyModelViewSet):
    queryset = Teacher.objects \
        .prefetch_related("emails", "external_links") \
        .all()
    serializer_class = TeacherSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend,)
    search_fields = ("first_name", "last_name", "about", "emails__email",
                     "external_links__url")
    filterset_fields = ("department",)
