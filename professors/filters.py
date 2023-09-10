from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, CharFilter

from professors.models import Professor


class ProfessorFilterSet(FilterSet):
    department = CharFilter(field_name="department__uuid", label=_("Department"))

    class Meta:
        model = Professor
        fields = ("department",)
