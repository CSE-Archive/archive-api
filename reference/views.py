from . import models
from . import serializers
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ReadOnlyModelViewSet


class ReferenceViewSet(ReadOnlyModelViewSet):
    queryset = models.Reference.objects \
        .prefetch_related("author_set") \
        .all()
    serializer_class = serializers.ReferenceSerializer
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = ("title", "author__full_name",)
    ordering_fields = ("date_modified", "date_created",)
