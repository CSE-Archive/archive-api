from .models import Email, ExternalLink, Teacher
from rest_framework import serializers
from django.utils.text import slugify


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ("email",)


class ExternalLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalLink
        fields = ("url",)


class SimpleTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ("id", "first_name", "last_name", "image", "department", "slug",)

    slug = serializers.SerializerMethodField(method_name="get_slug")

    def get_slug(self, teacher):
        return slugify(self.get_full_name(teacher), allow_unicode=True)


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ("id", "first_name", "last_name", "full_name", "image",
                  "department", "slug", "about", "emails", "external_links",)

    slug = serializers.SerializerMethodField(method_name="get_slug")
    emails = EmailSerializer(many=True, source="emails")
    external_links = ExternalLinkSerializer(
        many=True, source="external_links")
    full_name = serializers.SerializerMethodField(method_name="get_full_name")

    def get_full_name(self, teacher):
        return f"{teacher.first_name} {teacher.last_name}"

    def get_slug(self, teacher):
        return slugify(self.get_full_name(teacher), allow_unicode=True)
