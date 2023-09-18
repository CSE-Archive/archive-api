from django.db.models import Prefetch
from rest_framework.generics import ListAPIView

from chart.models import ChartNode
from chart.serializers import ChartNodeSerializer
from courses.models import CourseRelation


class ChartView(ListAPIView):
    queryset = ChartNode.objects \
        .select_related("course") \
        .prefetch_related(
            Prefetch(
                lookup="course__relations_to", to_attr="co_requisites",
                queryset=CourseRelation.objects.filter(type=CourseRelation.Types.CO).select_related("course_from")),
            Prefetch(
                lookup="course__relations_to", to_attr="pre_requisites",
                queryset=CourseRelation.objects.filter(type=CourseRelation.Types.PRE).select_related("course_from")),
            Prefetch(
                lookup="course__relations_from", to_attr="requisite_for",
                queryset=CourseRelation.objects.filter(type=CourseRelation.Types.PRE).select_related("course_to")),
            Prefetch(
                lookup="course__relations_from", to_attr="incompatibles_to",
                queryset=CourseRelation.objects.filter(type=CourseRelation.Types.INC).select_related("course_to")),
            Prefetch(
                lookup="course__relations_to", to_attr="incompatibles_from",
                queryset=CourseRelation.objects.filter(type=CourseRelation.Types.INC).select_related("course_from")),
        )
    serializer_class = ChartNodeSerializer
    pagination_class = None
