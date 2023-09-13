from rest_framework.viewsets import ReadOnlyModelViewSet

from professors.filters import ProfessorFilterSet
from professors.models import Department, Professor
from professors.serializers import (
    DepartmentListSerializer,
    ProfessorDetailSerializer,
    ProfessorListSerializer,
)


class DepartmentViewSet(ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    lookup_field = "uuid"
    serializer_class = DepartmentListSerializer
    search_fields = ("name", "name_en")


class ProfessorViewSet(ReadOnlyModelViewSet):
    queryset = Professor.objects \
        .select_related("department") \
        .prefetch_related("emails", "links")
    lookup_field = "uuid"
    filterset_class = ProfessorFilterSet
    search_fields = ("first_name", "last_name", "honorific",
                     "about", "emails__address", "links__url")

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "retrieve":
            queryset = queryset.prefetch_related(
                "classrooms__course"
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProfessorDetailSerializer
        return ProfessorListSerializer
