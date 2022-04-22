from rest_framework import serializers
from teacher.models import TeacherItem
from teacher.serializers import SimpleTeacherSerializer
from reference.models import ReferenceItem
from reference.serializers import SimpleReferenceSerializer


class TeacherItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherItem
        fields = ("teacher",)

    teacher = SimpleTeacherSerializer()


class ReferenceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceItem
        fields = ("reference",)

    reference = SimpleReferenceSerializer()
