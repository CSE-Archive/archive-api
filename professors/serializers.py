from typing import List
from operator import attrgetter

from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

from core.serializers import LinkSerializer
from courses.serializers.list import CourseListSerializer
from professors.models import Professor


class ProfessorListSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source="department.name")
    
    class Meta:
        model = Professor
        fields = ("uuid", "first_name", "last_name", "honorific",
                  "has_detail", "image", "department",)


class ProfessorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ("uuid", "first_name", "last_name", "honorific", "has_detail",
                  "image", "department", "about", "emails", "links", "courses",)

    links = LinkSerializer(many=True)
    emails = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()
    department = serializers.CharField(source="department.name")

    @swagger_serializer_method(serializers.ListField(child=serializers.CharField()))
    def get_emails(self, instance: Professor) -> List[str]:
        return instance.emails.values_list("address", flat=True)

    @swagger_serializer_method(CourseListSerializer(many=True))
    def get_courses(self, instance: Professor):
        return CourseListSerializer(set(map(attrgetter("course"), instance.classrooms.all())), many=True).data
