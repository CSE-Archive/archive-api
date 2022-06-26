from .models import Resource
from django_filters import FilterSet, NumberFilter


class ResourceFilterSet(FilterSet):
    course_id = NumberFilter(field_name="classroom__course_id")

    class Meta:
        model = Resource
        fields = ("course_id", "classroom_id", "type",)
