from rest_framework import serializers

from core.helpers import gregorian_to_jalali
from core.serializers import LinkSerializer
from references.models import Author, Reference


class AuthorSerializer(serializers.Serializer):
    def to_representation(self, instance: Author):
        return instance.full_name


class ReferenceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ("uuid", "title", "cover_image", "authors", "links",)
    
    links = LinkSerializer(many=True)
    authors = AuthorSerializer(many=True)


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ("uuid", "title", "notes", "cover_image", "authors", "courses",
                  "links", "related_references", "created_time", "modified_time",)
    
    links = LinkSerializer(many=True)
    authors = AuthorSerializer(many=True)
    courses = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()
    modified_time = serializers.SerializerMethodField()
    related_references = ReferenceListSerializer(many=True)

    def get_courses(self, instance: Reference):
        from courses.serializers import CourseListSerializer
        return CourseListSerializer(instance.courses, many=True).data

    def get_created_time(self, instance: Reference):
        return gregorian_to_jalali(instance.created_time)

    def get_modified_time(self, instance: Reference):
        return gregorian_to_jalali(instance.modified_time)
