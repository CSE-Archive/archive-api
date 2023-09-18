from typing import List
from operator import attrgetter

from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

from resources.serializers import ResourceListSerializer
from courses.serializers.list import CourseListSerializer
from professors.serializers import ProfessorListSerializer
from recordings.serializers import RecordedClassroomSerializer
from classrooms.models import Classroom


class ClassroomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ("uuid", "year", "semester", "course",
                  "tas", "professors", "resources", "recordings",)

    tas = serializers.SerializerMethodField()
    course = CourseListSerializer()
    resources = ResourceListSerializer(many=True)
    recordings = RecordedClassroomSerializer()
    professors = ProfessorListSerializer(many=True)

    @swagger_serializer_method(serializers.ListField(child=serializers.CharField()))
    def get_tas(self, instance: Classroom) -> List[str]:
        return map(attrgetter("full_name"), instance.tas.all())
