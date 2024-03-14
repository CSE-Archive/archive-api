from django.contrib import admin
from django.utils.translation import gettext_lazy as _
import nested_admin

from core.admin import BaseAdminMixin
from core.helpers import model_change_url_to_html, model_changelist_url_to_html
from classrooms.models import Classroom, TA
from recordings.admin import RecordedClassroomNestedInlineAdmin
from resources.admin import ResourceNestedInlineAdmin


class ClassroomInlineAdmin(admin.TabularInline):
    model = Classroom.tas.through
    extra = 0
    autocomplete_fields = ("classroom",)
    verbose_name = _("Classroom")
    verbose_name_plural = _("Classrooms")


@admin.register(Classroom)
class ClassroomAdmin(BaseAdminMixin, nested_admin.NestedModelAdmin):
    inlines = (ResourceNestedInlineAdmin, RecordedClassroomNestedInlineAdmin)
    autocomplete_fields = ("course", "professors", "tas",)
    list_per_page = 25
    list_display = ("uuid", "year", "semester", "course",
                    "tas_count", "professors_count",
                    "recordings_", "resources_count",)
    list_select_related = ("course", "recordings",)
    list_filter = ("year", "semester",)
    search_fields = ("uuid", "year", "semester",
                     "course__title", "course__en_title",
                     "tas__full_name", "professors__last_name",)

    @admin.display(ordering="tas_count", description=_("Number of TAs"))
    def tas_count(self, instance: Classroom):
        return model_changelist_url_to_html(
            app="classrooms",
            model="ta",
            query_key="classrooms",
            query_val=instance.id,
            placeholder=instance.tas.count(),
        )

    @admin.display(ordering="professors_count", description=_("Number of Professors"))
    def professors_count(self, instance: Classroom):
        return model_changelist_url_to_html(
            app="professors",
            model="professor",
            query_key="classrooms",
            query_val=instance.id,
            placeholder=instance.professors.count(),
        )

    @admin.display(description=_("Recordings"))
    def recordings_(self, instance: Classroom):
        return model_change_url_to_html(
            app="recordings",
            model="recordedclassroom",
            args=(instance.id,),
            placeholder=instance.recordings,
        )

    @admin.display(ordering="resources_count", description=_("Number of Resources"))
    def resources_count(self, instance: Classroom):
        return model_changelist_url_to_html(
            app="resources",
            model="resource",
            query_key="classroom",
            query_val=instance.id,
            placeholder=instance.resources.count(),
        )

    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related(
                "tas",
                "resources",
                "professors",
            )

@admin.register(TA)
class TAAdmin(admin.ModelAdmin):
    inlines = (ClassroomInlineAdmin,)
    list_per_page = 25
    list_display = ("id", "full_name", "classroom_count",)
    search_fields = ("full_name",)

    @admin.display(ordering="classroom_count", description=_("Number of Classrooms"))
    def classroom_count(self, instance: TA):
        return model_changelist_url_to_html(
            app="classrooms",
            model="classroom",
            query_key="tas",
            query_val=instance.id,
            placeholder=instance.classrooms.count(),
        )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            "classrooms",
        )
