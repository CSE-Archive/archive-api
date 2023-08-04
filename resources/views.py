from rest_framework.viewsets import ReadOnlyModelViewSet

from resources.models import Resource
from resources.filters import ResourceFilterSet
from resources.serializers import ResourceSerializer


class ResourceViewSet(ReadOnlyModelViewSet):
    queryset = Resource.objects \
        .select_related("classroom__course") \
        .prefetch_related(
            "links",
            "classroom__professors",
            "classroom__professors__department",
        )
    lookup_field = "uuid"
    serializer_class = ResourceSerializer
    filterset_class = ResourceFilterSet
    search_fields = ("title", "classroom__course__title",)
