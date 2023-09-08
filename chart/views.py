from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from chart.models import ChartNode
from chart.serializers import ChartNodeSerializer
from courses.models import Course, Requisite
from courses.serializers.list import CourseListSerializer


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
    pagination_class = None
