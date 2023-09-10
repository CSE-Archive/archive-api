from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, CharFilter

from references.models import Reference


class ReferenceFilterSet(FilterSet):
    course = CharFilter(field_name="course__uuid", label=_("Course"))

    class Meta:
        model = Reference
        fields = ("course", "type",)
