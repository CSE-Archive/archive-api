from rest_framework.viewsets import ReadOnlyModelViewSet

from classrooms.models import Classroom
from classrooms.serializers import ClassroomListSerializer, ClassroomDetailSerializer


class ClassroomViewSet(ReadOnlyModelViewSet):
    queryset = Classroom.objects \
        .select_related("course") \
        .prefetch_related(
            "tas",
            "professors",
            "professors__department",
            "resources",
            "resources__links",
            "recordings",
            "recordings__links",
        )
    lookup_field = "uuid"
    filterset_fields = ("year", "semester", "course_id",)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ClassroomDetailSerializer
        return ClassroomListSerializer
