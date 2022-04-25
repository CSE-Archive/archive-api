from . import models
from jdatetime import datetime as jdt
from rest_framework import serializers
from django.utils.timezone import localtime


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = ("full_name",)


class SimpleReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reference
        fields = ("id", "title", "url", "cover_image", "authors",)

    authors = AuthorSerializer(many=True, source="author_set")


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reference
        fields = ("id", "title", "url", "cover_image", "date_created",
                  "date_modified", "authors",)
    
    authors = AuthorSerializer(many=True, source="author_set")
    
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
    

class ReferenceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ReferenceItem
        fields = ("reference",)

    reference = SimpleReferenceSerializer()
