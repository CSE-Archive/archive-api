from . import models
from itertools import chain
from jdatetime import datetime as jdt
from rest_framework import serializers
from django.db.models import Q
from django.utils.timezone import localtime
from teacher.serializers import TeacherItemSerializer
from reference.serializers import ReferenceItemSerializer


class SimpleCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ("id", "title", "en_title", "unit",)


class SimpleSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Session
        fields = ("id", "year", "semester", "course", "teacher_items",)

    course = SimpleCourseSerializer()
    teacher_items = TeacherItemSerializer(many=True)


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


class DetailResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Resource
        fields = ("id", "title", "type", "url", "date_created",
                  "date_modified", "session",)

    date_created = serializers.SerializerMethodField(
        method_name="get_date_created")
    date_modified = serializers.SerializerMethodField(
        method_name="get_date_modified")
    session = SimpleSessionSerializer()

    def get_date_created(self, resource):
        return jdt.fromgregorian(
            date=localtime(resource.date_created)
        ).strftime("%Y-%m-%d %H:%M:%S")

    def get_date_modified(self, resource):
        return jdt.fromgregorian(
            date=localtime(resource.date_modified)
        ).strftime("%Y-%m-%d %H:%M:%S")


class ListSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Session
        fields = ("id", "year", "semester", "course", "teacher_items",)

    course = SimpleCourseSerializer()
    teacher_items = TeacherItemSerializer(many=True)


class DetailSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Session
        fields = ("id", "year", "semester", "course",
                  "tas", "teacher_items", "resources",)

    class ResourceSessionSerializer(DetailResourceSerializer):
        class Meta(DetailResourceSerializer.Meta):
            fields = ("id", "title", "type", "url", "date_created",
                      "date_modified",)

    course = SimpleCourseSerializer()
    teacher_items = TeacherItemSerializer(many=True)
    tas = TASerializer(source="ta_set", many=True)
    resources = ResourceSessionSerializer(source="resource_set", many=True)


class ListCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ("id", "title", "en_title", "unit", "type", "tag",
                  "description", "requisites",)

    requisites = serializers.SerializerMethodField(
        method_name="get_requisites")

    def get_requisites(self, course: models.Course):
        requisites = list(chain(course.requisites_from.all(), course.requisites_to.all()))
        return RequisiteSerializer(requisites, many=True).data


class DetailCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ("id", "title", "en_title", "unit", "type", "tag",
                  "description", "requisites", "reference_items", "sessions",)

    class SessionCourseSerializer(DetailSessionSerializer):
        class Meta(DetailSessionSerializer.Meta):
            fields = ("id", "year", "semester", "tas",
                      "teacher_items", "resources",)

    reference_items = ReferenceItemSerializer(many=True)
    requisites = serializers.SerializerMethodField(
        method_name="get_requisites")
    sessions = SessionCourseSerializer(source="session_set", many=True)

    def get_requisites(self, course: models.Course):
        requisites = list(chain(course.requisites_from.all(), course.requisites_to.all()))
        return RequisiteSerializer(requisites, many=True).data
