from django_filters import FilterSet, NumberFilter

from resources.models import Resource


class ResourceFilterSet(FilterSet):
    course = NumberFilter(field_name="classroom__course__uuid")
    classroom = NumberFilter(field_name="classroom__uuid")

    class Meta:
        model = Resource
        fields = ("course", "classroom", "type",)
