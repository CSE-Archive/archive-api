import jdatetime

from . import models
from rest_framework import serializers
from django.utils.timezone import localtime


class SimpleCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ("id", "title", "en_title", "unit",)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ("id", "title", "en_title", "unit",
                  "type", "tag", "description", "sessions",)

    sessions = serializers.PrimaryKeyRelatedField(
        source="session_set", many=True, read_only=True)


class RequisiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Requisite
        fields = ("type", "course_from", "course_to",)

    course_from = SimpleCourseSerializer()
    course_to = SimpleCourseSerializer()


class TASerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TA
        fields = ("full_name",)


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Session
        fields = ("id", "year", "semester", "course", "tas", "resources",)

    course = SimpleCourseSerializer()
    tas = TASerializer(many=True, source="ta_set")
    resources = serializers.PrimaryKeyRelatedField(
        source="resource_set", many=True, read_only=True)


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Resource
        fields = ("id", "title", "type", "url", "date_created", "date_modified", "session",)

    date_created = serializers.SerializerMethodField(
        method_name="get_date_created")
    date_modified = serializers.SerializerMethodField(
        method_name="get_date_modified")

    def get_date_created(self, resource):
        return jdatetime.datetime.fromgregorian(
            date=localtime(resource.date_created)
        ).strftime("%Y-%m-%d %H:%M:%S")

    def get_date_modified(self, resource):
        return jdatetime.datetime.fromgregorian(
            date=localtime(resource.date_modified)
        ).strftime("%Y-%m-%d %H:%M:%S")
