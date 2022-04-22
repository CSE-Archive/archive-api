from . import models
from . import serializers
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend


class TeacherViewSet(ReadOnlyModelViewSet):
    queryset = models.Teacher.objects \
        .prefetch_related("email_set", "externallink_set") \
        .all()
    serializer_class = serializers.TeacherSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend,)
    search_fields = ("first_name", "last_name", "about",)
    filterset_fields = ("department",)
