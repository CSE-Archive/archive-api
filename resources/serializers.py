from rest_framework import serializers

from core.helpers import gregorian_to_jalali
from core.serializers import LinkSerializer
from resources.models import Resource


class ResourceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ("uuid", "title", "type", "links")

    links = LinkSerializer(many=True)


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ("uuid", "title", "notes", "type", "classroom",
                  "links", "created_time", "modified_time",)

    links = LinkSerializer(many=True)
    classroom = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()
    modified_time = serializers.SerializerMethodField()

    def get_classroom(self, instance: Resource):
        from classrooms.serializers import ClassroomListSerializer
        return ClassroomListSerializer(instance.classroom).data

    def get_created_time(self, instance: Resource):
        return gregorian_to_jalali(instance.created_time)

    def get_modified_time(self, instance: Resource):
        return gregorian_to_jalali(instance.modified_time)
