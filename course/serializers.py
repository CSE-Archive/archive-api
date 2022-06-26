from .models import Classroom, Course, Resource, Requisite, TA
from jdatetime import datetime as jdt
from rest_framework import serializers
from django.utils.text import slugify
from django.utils.timezone import localtime
from teacher.serializers import TeacherItemSerializer
from reference.serializers import ReferenceItemSerializer


class SimpleCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "title", "en_title", "unit", "slug",)

    slug = serializers.SerializerMethodField(method_name="get_slug")

    def get_slug(self, course: Course):
        return slugify(course.title, allow_unicode=True)


class SimpleClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ("id", "year", "semester", "course", "teacher_items",)

    course = SimpleCourseSerializer()
    teacher_items = TeacherItemSerializer(many=True)


class RequisiteFromSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisite
        fields = ("type", "course",)

    course = SimpleCourseSerializer(source="course_to")


class RequisiteToSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisite
        fields = ("type", "course",)

    course = SimpleCourseSerializer(source="course_from")


class TASerializer(serializers.ModelSerializer):
    class Meta:
        model = TA
        fields = ("full_name",)


class DetailResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ("id", "title", "type", "url", "support_url", "date_created",
                  "date_modified", "classroom",)

    date_created = serializers.SerializerMethodField(
        method_name="get_date_created")
    date_modified = serializers.SerializerMethodField(
        method_name="get_date_modified")
    classroom = SimpleClassroomSerializer()

    def get_date_created(self, resource):
        return jdt.fromgregorian(
            date=localtime(resource.date_created)
        ).strftime("%Y-%m-%d %H:%M:%S")

    def get_date_modified(self, resource):
        return jdt.fromgregorian(
            date=localtime(resource.date_modified)
        ).strftime("%Y-%m-%d %H:%M:%S")


class ListClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ("id", "year", "semester", "course", "teacher_items",)

    course = SimpleCourseSerializer()
    teacher_items = TeacherItemSerializer(many=True)


class DetailClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ("id", "year", "semester", "course",
                  "tas", "teacher_items", "resources",)

    class ResourceClassroomSerializer(DetailResourceSerializer):
        class Meta(DetailResourceSerializer.Meta):
            fields = ("id", "title", "type", "url", "support_url", "date_created",
                      "date_modified",)

    course = SimpleCourseSerializer()
    teacher_items = TeacherItemSerializer(many=True)
    tas = TASerializer(source="tas", many=True)
    resources = ResourceClassroomSerializer(source="resources", many=True)


class ListCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "title", "en_title", "unit", "type", "tag", "slug",
                  "description", "requisites", "requisites_for",)

    slug = serializers.SerializerMethodField(method_name="get_slug")
    requisites = RequisiteToSerializer(source="requisites_to", many=True)
    requisites_for = RequisiteFromSerializer(
        source="requisites_from", many=True)

    def get_slug(self, course: Course):
        return slugify(course.title, allow_unicode=True)


class DetailCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "title", "en_title", "unit", "type", "tag", "slug",
                  "description", "requisites", "requisites_for",
                  "reference_items", "classrooms",)

    class ClassroomCourseSerializer(DetailClassroomSerializer):
        class Meta(DetailClassroomSerializer.Meta):
            fields = ("id", "year", "semester", "tas",
                      "teacher_items", "resources",)

    slug = serializers.SerializerMethodField(method_name="get_slug")
    requisites = RequisiteToSerializer(source="requisites_to", many=True)
    requisites_for = RequisiteFromSerializer(
        source="requisites_from", many=True)
    reference_items = ReferenceItemSerializer(many=True)
    classrooms = ClassroomCourseSerializer(source="classrooms", many=True)

    def get_slug(self, course: Course):
        return slugify(course.title, allow_unicode=True)
