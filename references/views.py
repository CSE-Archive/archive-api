from rest_framework.viewsets import ReadOnlyModelViewSet

from references.models import Reference
from references.filters import ReferenceFilterSet
from references.serializers import ReferenceListSerializer, ReferenceDetailSerializer


class ReferenceViewSet(ReadOnlyModelViewSet):
    queryset = Reference.objects \
        .prefetch_related(
            "links",
            "authors",
        )
    lookup_field = "uuid"
    filterset_class = ReferenceFilterSet
    search_fields = ("title", "collector", "authors__full_name",)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "retrieve":
            queryset = queryset.prefetch_related(
                "courses",
                "related_references",
                "related_references__links",
                "related_references__authors",
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ReferenceDetailSerializer
        return ReferenceListSerializer

