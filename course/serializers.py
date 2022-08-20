from core.helpers import gregorian_to_jalali
from .models import Classroom, Course, Resource, Requisite, TA
from rest_framework import serializers
from django.utils.text import slugify
from teacher.serializers import SimpleTeacherSerializer
from reference.serializers import SimpleReferenceSerializer


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
        fields = ("id", "year", "semester", "course", "teachers",)

    course = SimpleCourseSerializer()
    teachers = SimpleTeacherSerializer(many=True)


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
        fields = ("id", "title", "type", "file", "support_url", "date_created",
                  "date_modified", "classroom",)

    date_created = serializers.SerializerMethodField(
        method_name="get_date_created")
    date_modified = serializers.SerializerMethodField(
        method_name="get_date_modified")
    classroom = SimpleClassroomSerializer()

    def get_date_created(self, resource):
        return gregorian_to_jalali(resource.date_created)

    def get_date_modified(self, resource):
        return gregorian_to_jalali(resource.date_modified)


class ListClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ("id", "year", "semester", "course", "teachers",)

    course = SimpleCourseSerializer()
    teachers = SimpleTeacherSerializer(many=True)


class DetailClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ("id", "year", "semester", "course",
                  "tas", "teachers", "resources",)

    class ResourceClassroomSerializer(DetailResourceSerializer):
        class Meta(DetailResourceSerializer.Meta):
            fields = ("id", "title", "type", "file", "support_url",
                      "date_created", "date_modified",)

    course = SimpleCourseSerializer()
    teachers = SimpleTeacherSerializer(many=True)
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
                  "references", "classrooms",)

    class ClassroomCourseSerializer(DetailClassroomSerializer):
        class Meta(DetailClassroomSerializer.Meta):
            fields = ("id", "year", "semester", "tas",
                      "teachers", "resources",)

    slug = serializers.SerializerMethodField(method_name="get_slug")
    requisites = RequisiteToSerializer(source="requisites_to", many=True)
    requisites_for = RequisiteFromSerializer(
        source="requisites_from", many=True)
    references = SimpleReferenceSerializer(many=True)
    classrooms = ClassroomCourseSerializer(source="classrooms", many=True)

    def get_slug(self, course: Course):
        return slugify(course.title, allow_unicode=True)
