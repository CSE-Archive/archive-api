from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from chart.models import ChartNode
from chart.serializers import ChartNodeSerializer
from courses.models import Course, Requisite
from courses.serializers import CourseListSerializer


class ChartView(ListAPIView):
    queryset = ChartNode.objects \
        .select_related("course") \
        .prefetch_related(
            Prefetch(
                lookup="course__requisites_to", to_attr="co_requisites",
                queryset=Requisite.objects.filter(type=Requisite.Types.CO).select_related("course_from")),
            Prefetch(
                lookup="course__requisites_to", to_attr="pre_requisites",
                queryset=Requisite.objects.filter(type=Requisite.Types.PRE).select_related("course_from")),
            Prefetch(
                lookup="course__requisites_from", to_attr="requisite_for",
                queryset=Requisite.objects.filter(type=Requisite.Types.PRE).select_related("course_to"))
        )
    serializer_class = ChartNodeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            "nodes": serializer.data,
            "extra": {
                str(Course.Types.GENERAL): CourseListSerializer(Course.objects.filter(type=Course.Types.GENERAL, chart_node__isnull=True), many=True).data,
                str(Course.Types.OPTIONAL): CourseListSerializer(Course.objects.filter(type=Course.Types.OPTIONAL, chart_node__isnull=True), many=True).data
            }
        }
        return Response(data)
