from .models import Author, Reference
from jdatetime import datetime as jdt
from rest_framework import serializers
from django.utils.timezone import localtime


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
        return jdt.fromgregorian(
            date=localtime(resource.date_created)
        ).strftime("%Y-%m-%d %H:%M:%S")

    def get_date_modified(self, resource):
        return jdt.fromgregorian(
            date=localtime(resource.date_modified)
        ).strftime("%Y-%m-%d %H:%M:%S")
