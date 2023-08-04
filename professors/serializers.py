from operator import attrgetter

from rest_framework import serializers

from core.serializers import LinkSerializer
from professors.models import Professor


class ProfessorListSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source="department.name")
    
    class Meta:
        model = Professor
        fields = ("uuid", "first_name", "last_name", "honorific",
                  "has_detail", "image", "department",)


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ("uuid", "first_name", "last_name", "honorific", "has_detail",
                  "image", "department", "about", "emails", "links", "courses",)

    links = LinkSerializer(many=True)
    emails = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()
    department = serializers.CharField(source="department.name")

    def get_courses(self, instance: Professor):
        from courses.serializers import CourseListSerializer
        return CourseListSerializer(map(attrgetter("course"), instance.classrooms.all()), many=True).data
    
    def get_emails(self, instance: Professor):
        return instance.emails.values_list("address", flat=True)
