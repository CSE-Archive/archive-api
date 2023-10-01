from typing import List
from operator import attrgetter

from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

from courses.serializers.list import CourseListSerializer
from professors.serializers import ProfessorListSerializer
from classrooms.models import Classroom


class ClassroomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ("uuid", "year", "semester", "course", "professors",)

    tas = serializers.SerializerMethodField()
    course = CourseListSerializer()
    professors = ProfessorListSerializer(many=True)

    @swagger_serializer_method(serializers.ListField(child=serializers.CharField()))
    def get_tas(self, instance: Classroom) -> List[str]:
        return map(attrgetter("full_name"), instance.tas.all())
