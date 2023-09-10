from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet

from courses.models import Course, Requisite
from courses.serializers import CourseListSerializer, CourseDetailSerializer


class CourseViewSet(ReadOnlyModelViewSet):
    queryset = Course.objects \
        .prefetch_related(
            "references",
            "references__links",
            "references__writers",
            "classrooms__professors",
            "classrooms__professors__department",
            "classrooms__resources",
            "classrooms__resources__links",
            "classrooms__recordings",
            "classrooms__recordings__links",
            "classrooms__tas",
        )
    lookup_field = "uuid"
    filterset_fields = ("type", "units",)
    search_fields = ("title", "en_title", "description", "tag",)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "retrieve":
            queryset = queryset.prefetch_related(
                Prefetch(
                    lookup="requisites_to", to_attr="co_requisites",
                    queryset=Requisite.objects.filter(type=Requisite.Types.CO).select_related("course_from")),
                Prefetch(
                    lookup="requisites_to", to_attr="pre_requisites",
                    queryset=Requisite.objects.filter(type=Requisite.Types.PRE).select_related("course_from")),
                Prefetch(
                    lookup="requisites_from", to_attr="requisite_for",
                    queryset=Requisite.objects.filter(type=Requisite.Types.PRE).select_related("course_to"))
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseListSerializer
