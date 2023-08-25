from rest_framework import serializers

from courses.models import Course


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("uuid", "title", "units", "type",)
