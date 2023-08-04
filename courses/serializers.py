from django.db.models import Q
from rest_framework import serializers

from references.serializers import ReferenceListSerializer
from classrooms.serializers import ClassroomSerializer
from professors.serializers import ProfessorListSerializer
from courses.models import Course, Requisite
from professors.models import Professor


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("uuid", "title", "en_title", "unit", "type",)


class RequisiteFromSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisite
        fields = ("course_from",)
    
    course_from = CourseListSerializer()

    def to_representation(self, instance):
        return super().to_representation(instance)["course_from"]


class RequisiteToSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisite
        fields = ("course_to",)
    
    course_to = CourseListSerializer()

    def to_representation(self, instance):
        return super().to_representation(instance)["course_to"]


class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("uuid", "title", "en_title", "unit", "type", "tag", "known_as",
                  "description", "references", "classrooms", "professors",
                  "co_requisites", "pre_requisites", "requisite_for",)

    references = ReferenceListSerializer(many=True)
    classrooms = ClassroomSerializer(many=True)
    professors = serializers.SerializerMethodField()
    co_requisites = RequisiteFromSerializer(many=True)
    pre_requisites = RequisiteFromSerializer(many=True)
    requisite_for = RequisiteToSerializer(many=True)

    def get_professors(self, instance: Course):
        queryset = Professor.objects.filter(
            classrooms__course=obj,
        ).select_related("department").distinct()
        return ProfessorListSerializer(queryset, many=True).data
