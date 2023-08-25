from typing import List

from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

from core.helpers import gregorian_to_jalali
from core.serializers import LinkSerializer
from courses.serializers.list import CourseListSerializer
from references.models import Reference


class ReferenceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ("uuid", "title", "type", "cover_image", "collector", "authors", "links",)
    
    links = LinkSerializer(many=True)
    authors = serializers.SerializerMethodField()

    @swagger_serializer_method(serializers.ListField(child=serializers.CharField()))
    def get_authors(self, instance: Reference) -> List[str]:
        return instance.authors.values_list("full_name", flat=True)


class ReferenceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ("uuid", "title", "type", "notes", "cover_image", "collector", "authors", "courses",
                  "links", "related_references", "created_time", "modified_time",)
    
    links = LinkSerializer(many=True)
    authors = serializers.SerializerMethodField()
    courses = CourseListSerializer(many=True)
    created_time = serializers.SerializerMethodField()
    modified_time = serializers.SerializerMethodField()
    related_references = ReferenceListSerializer(many=True)

    @swagger_serializer_method(serializers.ListField(child=serializers.CharField()))
    def get_authors(self, instance: Reference) -> List[str]:
        return instance.authors.values_list("full_name", flat=True)

    def get_created_time(self, instance: Reference) -> str:
        return gregorian_to_jalali(instance.created_time)

    def get_modified_time(self, instance: Reference) -> str:
        return gregorian_to_jalali(instance.modified_time)
