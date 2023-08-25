from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

from references.serializers import ReferenceListSerializer
from professors.serializers import ProfessorListSerializer
from classrooms.serializers.detail import ClassroomDetailSerializer
from courses.serializers.requisite import RequisiteFromSerializer, RequisiteToSerializer
from courses.models import Course
from professors.models import Professor


class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("uuid", "title", "en_title", "units", "type", "tag", "known_as",
                  "description", "references", "classrooms", "professors",
                  "co_requisites", "pre_requisites", "requisite_for",)

    references = ReferenceListSerializer(many=True)
    classrooms = ClassroomDetailSerializer(many=True)
    professors = serializers.SerializerMethodField()
    co_requisites = RequisiteFromSerializer(many=True)
    pre_requisites = RequisiteFromSerializer(many=True)
    requisite_for = RequisiteToSerializer(many=True)

    @swagger_serializer_method(ProfessorListSerializer(many=True))
    def get_professors(self, instance: Course):
        queryset = Professor.objects.filter(
            classrooms__course=instance,
        ).select_related("department").distinct()
        return ProfessorListSerializer(queryset, many=True).data
