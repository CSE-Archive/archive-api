from core.helpers import gregorian_to_jalali
from .models import Author, Reference
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("full_name",)


class SimpleReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ("id", "title", "file", "support_url", "cover_image", "authors",)

    authors = AuthorSerializer(many=True, source="authors")


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ("id", "title", "file", "support_url", "cover_image", "date_created",
                  "date_modified", "authors",)
    
    authors = AuthorSerializer(many=True, source="authors")
    
    date_created = serializers.SerializerMethodField(
        method_name="get_date_created")
    date_modified = serializers.SerializerMethodField(
        method_name="get_date_modified")

    def get_date_created(self, resource):
        return gregorian_to_jalali(resource.date_created)

    def get_date_modified(self, resource):
        return gregorian_to_jalali(resource.date_modified)
