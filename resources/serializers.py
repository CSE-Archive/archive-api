from rest_framework import serializers

from core.helpers import gregorian_to_jalali
from core.serializers import LinkSerializer
from classrooms.serializers.list import ClassroomListSerializer
from resources.models import Resource


class ResourceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ("uuid", "title", "type", "file", "links",)

    links = LinkSerializer(many=True)


class ResourceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ("uuid", "title", "notes", "type", "file", "classroom",
                  "links", "created_time", "modified_time",)

    links = LinkSerializer(many=True)
    classroom = ClassroomListSerializer()
    created_time = serializers.SerializerMethodField()
    modified_time = serializers.SerializerMethodField()

    def get_created_time(self, instance: Resource) -> str:
        return gregorian_to_jalali(instance.created_time)

    def get_modified_time(self, instance: Resource) -> str:
        return gregorian_to_jalali(instance.modified_time)
