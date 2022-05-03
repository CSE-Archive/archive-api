from . import models
from jdatetime import datetime as jdt
from rest_framework import serializers
from django.utils.text import slugify
from django.utils.timezone import localtime
from teacher.serializers import TeacherItemSerializer
from reference.serializers import ReferenceItemSerializer


class SimpleCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ("id", "title", "en_title", "unit", "slug",)

    slug = serializers.SerializerMethodField(method_name="get_slug")

    def get_slug(self, course: models.Course):
        return slugify(course.title, allow_unicode=True)


class SimpleSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Session
        fields = ("id", "year", "semester", "course", "teacher_items",)

    course = SimpleCourseSerializer()
    teacher_items = TeacherItemSerializer(many=True)


class RequisiteFromSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Requisite
        fields = ("type", "course",)

    course = SimpleCourseSerializer(source="course_to")


class RequisiteToSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Requisite
        fields = ("type", "course",)

    course = SimpleCourseSerializer(source="course_from")


class TASerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TA
        fields = ("full_name",)


class DetailResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Resource
        fields = ("id", "title", "type", "url", "support_url", "date_created",
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
            fields = ("id", "title", "type", "url", "support_url", "date_created",
                      "date_modified",)

    course = SimpleCourseSerializer()
    teacher_items = TeacherItemSerializer(many=True)
    tas = TASerializer(source="ta_set", many=True)
    resources = ResourceSessionSerializer(source="resource_set", many=True)


class ListCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ("id", "title", "en_title", "unit", "type", "tag", "slug",
                  "description", "requisites", "requisites_for",)

    slug = serializers.SerializerMethodField(method_name="get_slug")
    requisites = RequisiteToSerializer(source="requisites_to", many=True)
    requisites_for = RequisiteFromSerializer(
        source="requisites_from", many=True)

    def get_slug(self, course: models.Course):
        return slugify(course.title, allow_unicode=True)


class DetailCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ("id", "title", "en_title", "unit", "type", "tag", "slug",
                  "description", "requisites", "requisites_for",
                  "reference_items", "sessions",)

    class SessionCourseSerializer(DetailSessionSerializer):
        class Meta(DetailSessionSerializer.Meta):
            fields = ("id", "year", "semester", "tas",
                      "teacher_items", "resources",)

    slug = serializers.SerializerMethodField(method_name="get_slug")
    requisites = RequisiteToSerializer(source="requisites_to", many=True)
    requisites_for = RequisiteFromSerializer(
        source="requisites_from", many=True)
    reference_items = ReferenceItemSerializer(many=True)
    sessions = SessionCourseSerializer(source="session_set", many=True)

    def get_slug(self, course: models.Course):
        return slugify(course.title, allow_unicode=True)
