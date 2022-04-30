from . import models
from rest_framework import serializers
from django.utils.text import slugify


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Email
        fields = ("email",)


class ExternalLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExternalLink
        fields = ("url",)


class SimpleTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ("id", "full_name", "image", "department", "slug",)

    full_name = serializers.SerializerMethodField(method_name="get_full_name")
    slug = serializers.SerializerMethodField(method_name="get_slug")

    def get_full_name(self, teacher):
        return f"{teacher.first_name} {teacher.last_name}"

    def get_slug(self, teacher):
        return slugify(self.get_full_name(teacher), allow_unicode=True)


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teacher
        fields = ("id", "first_name", "last_name", "full_name", "image",
                  "department", "slug", "about", "emails", "external_links",)

    slug = serializers.SerializerMethodField(method_name="get_slug")
    emails = EmailSerializer(many=True, source="email_set")
    external_links = ExternalLinkSerializer(
        many=True, source="externallink_set")
    full_name = serializers.SerializerMethodField(method_name="get_full_name")

    def get_full_name(self, teacher):
        return f"{teacher.first_name} {teacher.last_name}"

    def get_slug(self, teacher):
        return slugify(self.get_full_name(teacher), allow_unicode=True)


class TeacherItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TeacherItem
        fields = ("teacher",)

    teacher = SimpleTeacherSerializer()
