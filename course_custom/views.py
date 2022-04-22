from . import serializers
from django.contrib.contenttypes.models import ContentType
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from course.models import Course, Session
from teacher.models import TeacherItem
from reference.models import ReferenceItem


class TeacherItemViewSet(ListModelMixin, GenericViewSet):
    serializer_class = serializers.TeacherItemSerializer

    def get_queryset(self):
        return TeacherItem.objects \
            .select_related("teacher") \
            .filter(
                content_type=ContentType.objects.get_for_model(Session),
                object_id=self.kwargs["session_pk"]
            )


class ReferenceItemViewSet(ListModelMixin, GenericViewSet):
    serializer_class = serializers.ReferenceItemSerializer

    def get_queryset(self):
        return ReferenceItem.objects \
            .select_related("reference") \
            .prefetch_related("reference__author_set") \
            .filter(
                content_type=ContentType.objects.get_for_model(Course),
                object_id=self.kwargs["course_pk"]
            )
