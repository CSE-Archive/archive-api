from .models import Reference
from .serializers import ReferenceSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet


class ReferenceViewSet(ReadOnlyModelViewSet):
    queryset = Reference.objects \
        .prefetch_related("authors") \
        .all()
    serializer_class = ReferenceSerializer
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ("title", "author__full_name",)
    ordering_fields = ("date_modified", "date_created",)
