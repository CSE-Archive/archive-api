from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

from references.serializers import ReferenceListSerializer
from professors.serializers import ProfessorListSerializer
from classrooms.serializers.detail import ClassroomDetailSerializer
from courses.serializers.relation import RequisiteFromSerializer, RequisiteToSerializer
from courses.models import Course
from professors.models import Professor


class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("uuid", "title", "en_title", "units", "type", "tag", "known_as",
                  "description", "references", "classrooms", "professors",
                  "co_requisites", "pre_requisites", "requisite_for", "incompatibles",)

    references = ReferenceListSerializer(many=True)
    classrooms = ClassroomDetailSerializer(many=True)
    professors = serializers.SerializerMethodField()
    co_requisites = RequisiteFromSerializer(many=True)
    pre_requisites = RequisiteFromSerializer(many=True)
    requisite_for = RequisiteToSerializer(many=True)
    incompatibles = serializers.SerializerMethodField()

    @swagger_serializer_method(ProfessorListSerializer(many=True))
    def get_professors(self, instance: Course):
        queryset = Professor.objects.filter(
            classrooms__course=instance,
        ).select_related("department").distinct()
        context = {"request": self.context.get("request", None)}
        return ProfessorListSerializer(queryset, many=True, context=context).data

    @swagger_serializer_method(serializers.ListField(child=serializers.CharField()))
    def get_incompatibles(self, instance: Course):
        incompatibles_to = RequisiteToSerializer(instance.incompatibles_to, many=True)
        incompatibles_from = RequisiteFromSerializer(instance.incompatibles_from, many=True)
        return incompatibles_to.data + incompatibles_from.data
