from rest_framework import serializers

from courses.models import CourseRelation
from courses.serializers.list import CourseListSerializer


class RequisiteFromSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRelation
        fields = ("course_from",)
    
    course_from = CourseListSerializer()

    def to_representation(self, instance):
        return super().to_representation(instance)["course_from"]


class RequisiteToSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRelation
        fields = ("course_to",)
    
    course_to = CourseListSerializer()

    def to_representation(self, instance):
        return super().to_representation(instance)["course_to"]
