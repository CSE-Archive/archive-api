from typing import List
from operator import attrgetter

from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

from core.serializers import LinkSerializer
from courses.serializers.list import CourseListSerializer
from professors.models import Department, Professor


class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("uuid", "name", "name_en", "tag",)


class ProfessorListSerializer(serializers.ModelSerializer):
    department = DepartmentListSerializer()
    
    class Meta:
        model = Professor
        fields = ("uuid", "first_name", "last_name", "honorific", "image",
                  "department",)


class ProfessorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ("uuid", "first_name", "last_name", "honorific", "image",
                  "department", "about", "emails", "links", "courses",)

    links = LinkSerializer(many=True)
    emails = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()
    department = DepartmentListSerializer()

    @swagger_serializer_method(serializers.ListField(child=serializers.CharField()))
    def get_emails(self, instance: Professor) -> List[str]:
        return map(attrgetter("address"), instance.emails.all())

    @swagger_serializer_method(CourseListSerializer(many=True))
    def get_courses(self, instance: Professor):
        return CourseListSerializer(set(map(attrgetter("course"), instance.classrooms.all())), many=True).data
