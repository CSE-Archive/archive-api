from rest_framework.viewsets import ReadOnlyModelViewSet

from recordings.models import RecordedClassroom
from recordings.filters import RecordedClassroomFilterSet
from recordings.serializers import RecordedClassroomSerializer


class RecordedClassroomViewSet(ReadOnlyModelViewSet):
    queryset = RecordedClassroom.objects \
        .select_related("classroom__course") \
        .prefetch_related(
            "links",
            "sessions",
            "sessions__links",
            "classroom__professors",
            "classroom__professors__department",
        )
    lookup_field = "uuid"
    serializer_class = RecordedClassroomSerializer
    filterset_class = RecordedClassroomFilterSet
    search_fields = ("classroom__professors__first_name", "classroom__professors__last_name",
                     "classroom__course__title",)
