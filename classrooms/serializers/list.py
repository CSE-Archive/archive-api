from rest_framework import serializers

from courses.serializers.list import CourseListSerializer
from professors.serializers import ProfessorListSerializer
from classrooms.models import Classroom


class ClassroomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ("uuid", "year", "semester", "course", "professors",)

    course = CourseListSerializer()
    professors = ProfessorListSerializer(many=True)
