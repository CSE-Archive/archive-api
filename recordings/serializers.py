from rest_framework import serializers

from core.serializers import LinkSerializer
from classrooms.serializers.list import ClassroomListSerializer
from core.helpers import gregorian_to_jalali
from recordings.models import RecordedClassroom, RecordedSession


class RecordedSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordedSession
        fields = ("title", "links",)
    
    links = LinkSerializer(many=True)


class RecordedClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordedClassroom
        fields = ("uuid", "classroom", "notes", "sessions", "links",
                  "created_time", "modified_time",)

    links = LinkSerializer(many=True)
    sessions = RecordedSessionSerializer(many=True)
    classroom = ClassroomListSerializer()
    created_time = serializers.SerializerMethodField()
    modified_time = serializers.SerializerMethodField()

    def get_created_time(self, instance: RecordedClassroom) -> str:
        return gregorian_to_jalali(instance.created_time)

    def get_modified_time(self, instance: RecordedClassroom) -> str:
        return gregorian_to_jalali(instance.modified_time)
