from django_filters import FilterSet, NumberFilter

from recordings.models import RecordedClassroom


class RecordedClassroomFilterSet(FilterSet):
    course = NumberFilter(field_name="classroom__course__uuid")
    classroom = NumberFilter(field_name="classroom__uuid")

    class Meta:
        model = RecordedClassroom
        fields = ("course", "classroom",)
