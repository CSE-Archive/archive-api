from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

from chart.models import ChartNode
from courses.models import Course
from courses.serializers import RequisiteFromSerializer, RequisiteToSerializer


class ChartNodeCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("uuid", "title", "en_title", "units", "type",
                  "co_requisites", "pre_requisites", "requisite_for", "incompatibles",)
    
    co_requisites = RequisiteFromSerializer(many=True)
    pre_requisites = RequisiteFromSerializer(many=True)
    requisite_for = RequisiteToSerializer(many=True)
    incompatibles = serializers.SerializerMethodField()

    @swagger_serializer_method(serializers.ListField(child=serializers.CharField()))
    def get_incompatibles(self, instance: Course):
        incompatibles_to = RequisiteToSerializer(instance.incompatibles_to, many=True)
        incompatibles_from = RequisiteFromSerializer(instance.incompatibles_from, many=True)
        return incompatibles_to.data + incompatibles_from.data


class ChartNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartNode
        fields = ("semester", "column", "course", "type", "units",)

    course = ChartNodeCourseSerializer()
