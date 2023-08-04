from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.helpers import model_change_url_to_html
from chart.models import ChartNode


@admin.register(ChartNode)
class ChartNodeAdmin(admin.ModelAdmin):
    list_per_page = 100
    list_display = ("id", "course_", "type_", "semester", "column",)
    list_select_related = ("course",)

    @admin.display(ordering="course_", description=_("Course"))
    def course_(self, instance: ChartNode):
        if instance.course is None:
            return "-"
        return model_change_url_to_html(
            app="courses",
            model="course",
            args=(instance.course.id,),
            placeholder=instance.course,
        )

    @admin.display(ordering="type_", description=_("Type"))
    def type_(self, instance: ChartNode):
        if instance.course is None:
            return instance.get_type_display()
        return instance.course.get_type_display()
