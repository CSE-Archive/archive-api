from . import models
from . import serializers
from django.db.models import Q
from rest_framework.mixins import ListModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend


class CourseViewSet(ReadOnlyModelViewSet):
    queryset = models.Course.objects.prefetch_related("session_set").all()
    serializer_class = serializers.CourseSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filterset_fields = ("type", "unit",)
    search_fields = ("title", "en_title", "description", "tag",)


class RequisitesViewSet(ListModelMixin, GenericViewSet):
    serializer_class = serializers.RequisiteSerializer

    def get_queryset(self):
        return models.Requisite.objects \
            .select_related("course_from", "course_to") \
            .filter(
                Q(course_from__id=self.kwargs["course_pk"]) | Q(course_to__id=self.kwargs["course_pk"]))


class SessionViewSet(ReadOnlyModelViewSet):
    queryset = models.Session.objects.prefetch_related(
        "ta_set", "resource_set").all()
    serializer_class = serializers.SessionSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("year", "semester", "course_id",)


class ResourceViewSet(ReadOnlyModelViewSet):
    queryset = models.Resource.objects.all()
    serializer_class = serializers.ResourceSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filterset_fields = ("session_id", "session__course_id", "type",)
    search_fields = ("title",)
    ordering_fields = ("date_modified", "date_created",)
