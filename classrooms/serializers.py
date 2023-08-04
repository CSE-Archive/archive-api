from rest_framework import serializers

from resources.serializers import ResourceListSerializer
from professors.serializers import ProfessorListSerializer
from recordings.serializers import RecordedClassroomSerializer
from classrooms.models import TA, Classroom


class TaSerializer(serializers.Serializer):
    def to_representation(self, instance: TA):
        return instance.full_name


class ClassroomListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ("uuid", "year", "semester", "course", "professors",)

    course = serializers.SerializerMethodField()
    professors = ProfessorListSerializer(many=True)

    def get_course(self, instance: Classroom):
        from courses.serializers import CourseListSerializer
        return CourseListSerializer(instance.course).data


class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ("uuid", "year", "semester", "course",
                  "tas", "professors", "resources", "recordings",)

    tas = TaSerializer(many=True)
    course = serializers.SerializerMethodField()
    resources = ResourceListSerializer(many=True)
    recordings = RecordedClassroomSerializer()
    professors = ProfessorListSerializer(many=True)

    def get_course(self, instance: Classroom):
        from courses.serializers import CourseListSerializer
        return CourseListSerializer(instance.course).data
