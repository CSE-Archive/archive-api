from django_filters import FilterSet, NumberFilter

from references.models import Reference


class ReferenceFilterSet(FilterSet):
    course = NumberFilter(field_name="course__uuid")

    class Meta:
        model = Reference
        fields = ("course",)
