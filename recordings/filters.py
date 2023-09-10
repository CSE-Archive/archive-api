from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, CharFilter

from recordings.models import RecordedClassroom


class RecordedClassroomFilterSet(FilterSet):
    course = CharFilter(field_name="classroom__course__uuid", label=_("Course"))
    classroom = CharFilter(field_name="classroom__uuid", label=_("Classroom"))

    class Meta:
        model = RecordedClassroom
        fields = ("course", "classroom",)
