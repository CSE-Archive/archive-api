from rest_framework import serializers

from chart.models import ChartNode
from courses.models import Course
from courses.serializers import RequisiteFromSerializer, RequisiteToSerializer


class ChartNodeCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("uuid", "title", "en_title", "unit", "type",
                  "co_requisites", "pre_requisites", "requisite_for",)
    
    co_requisites = RequisiteFromSerializer(many=True)
    pre_requisites = RequisiteFromSerializer(many=True)
    requisite_for = RequisiteToSerializer(many=True)


class ChartNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartNode
        fields = ("semester", "column", "course", "type", "unit",)

    course = ChartNodeCourseSerializer()
