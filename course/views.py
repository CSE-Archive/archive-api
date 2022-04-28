from . import models
from . import serializers
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend


class CourseViewSet(ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filterset_fields = ("type", "unit",)
    search_fields = ("title", "en_title", "description", "tag",)

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.ListCourseSerializer
        return serializers.DetailCourseSerializer

    def get_queryset(self):
        if self.action == "list":
            return models.Course.objects \
                .prefetch_related(
                    "requisites_from__course_to",
                    "requisites_to__course_from",
                )\
                .all()
        return models.Course.objects \
            .prefetch_related(
                "requisites_from__course_to",
                "requisites_to__course_from",
                "session_set__ta_set",
                "session_set__resource_set",
                "session_set__teacher_items__teacher",
                "reference_items__reference__author_set",) \
            .all()


class SessionViewSet(ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("year", "semester", "course_id",)

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.ListSessionSerializer
        return serializers.DetailSessionSerializer

    def get_queryset(self):
        if self.action == "list":
            return models.Session.objects \
                .prefetch_related("teacher_items__teacher") \
                .all()
        return models.Session.objects \
            .prefetch_related("ta_set", "resource_set", "teacher_items__teacher") \
            .all()


class ResourceViewSet(ReadOnlyModelViewSet):
    queryset = models.Resource.objects\
        .select_related("session__course")\
        .prefetch_related("session__teacher_items__teacher") \
        .all()
    serializer_class = serializers.DetailResourceSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filterset_fields = ("session_id", "session__course_id", "type",)
    search_fields = ("title",)
    ordering_fields = ("date_modified", "date_created",)
