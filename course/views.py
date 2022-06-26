from .models import Classroom, Course, Resource
from .filters import ResourceFilterSet
from .serializers import (ListCourseSerializer, DetailCourseSerializer,
                            ListClassroomSerializer, DetailClassroomSerializer,
                            DetailResourceSerializer)
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend


class CourseViewSet(ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filterset_fields = ("type", "unit",)
    search_fields = ("title", "en_title", "description", "tag",)

    def get_serializer_class(self):
        if self.action == "list":
            return ListCourseSerializer
        return DetailCourseSerializer

    def get_queryset(self):
        if self.action == "list":
            return Course.objects \
                .prefetch_related(
                    "requisites_from__course_to",
                    "requisites_to__course_from",
                )\
                .all()
        return Course.objects \
            .prefetch_related(
                "requisites_from__course_to",
                "requisites_to__course_from",
                "classrooms__tas",
                "classrooms__resources",
                "classrooms__teacher_items__teacher",
                "reference_items__reference__authors",) \
            .all()


class ClassroomViewSet(ReadOnlyModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("year", "semester", "course_id",)

    def get_serializer_class(self):
        if self.action == "list":
            return ListClassroomSerializer
        return DetailClassroomSerializer

    def get_queryset(self):
        if self.action == "list":
            return Classroom.objects \
                .prefetch_related("teacher_items__teacher") \
                .all()
        return Classroom.objects \
            .prefetch_related("tas", "resources", "teacher_items__teacher") \
            .all()


class ResourceViewSet(ReadOnlyModelViewSet):
    queryset = Resource.objects\
        .select_related("classroom__course")\
        .prefetch_related("classroom__teacher_items__teacher") \
        .all()
    serializer_class = DetailResourceSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filterset_class = ResourceFilterSet
    search_fields = ("title",)
    ordering_fields = ("date_modified", "date_created",)
