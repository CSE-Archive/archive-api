from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, CharFilter

from resources.models import Resource


class ResourceFilterSet(FilterSet):
    course = CharFilter(field_name="classroom__course__uuid", label=_("Course"))
    classroom = CharFilter(field_name="classroom__uuid", label=_("Classroom"))

    class Meta:
        model = Resource
        fields = ("course", "classroom", "type",)
