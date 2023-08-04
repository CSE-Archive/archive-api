from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet
from courses.models import Course

from professors.models import Professor
from professors.serializers import ProfessorSerializer, ProfessorListSerializer


class ProfessorViewSet(ReadOnlyModelViewSet):
    queryset = Professor.objects \
        .filter(has_detail=True) \
        .select_related("department") \
        .prefetch_related("emails", "links")
    lookup_field = "uuid"
    search_fields = ("first_name", "last_name", "honorific",
                     "about", "emails__email", "links__url")
    filterset_fields = ("department",)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "retrieve":
            queryset = queryset.prefetch_related(
                "classrooms__course"
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProfessorSerializer
        return ProfessorListSerializer
