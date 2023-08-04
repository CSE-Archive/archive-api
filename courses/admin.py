from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from core.admin import BaseAdminMixin
from courses.models import Course, Requisite
from core.helpers import model_change_url_to_html, model_changelist_url_to_html


class RequisiteFromInlineAdmin(admin.TabularInline):
    fk_name = "course_from"
    model = Requisite
    autocomplete_fields = ("course_to",)
    extra = 0
    verbose_name = _("Requisite")
    verbose_name_plural = _("Requisities")


class RequisiteToInlineAdmin(admin.TabularInline):
    fk_name = "course_to"
    model = Requisite
    autocomplete_fields = ("course_from",)
    extra = 0
    verbose_name = _("Requisite")
    verbose_name_plural = _("Requisities")


@admin.register(Course)
class CourseAdmin(BaseAdminMixin, admin.ModelAdmin):
    inlines = (RequisiteFromInlineAdmin, RequisiteToInlineAdmin,)
    list_per_page = 25
    list_display = ("uuid", "title", "en_title", "unit", "type",
                    "requisites_from_count", "requisites_to_count", "classrooms_count",
                    "references_count", "resources_count", "recordings_count",)
    search_fields = ("uuid", "title", "en_title", "description", "tag",)
    list_filter = ("type", "unit",)

    @admin.display(ordering="requisites_from_count", description=_("Number of Requisities-From"))
    def requisites_from_count(self, instance: Course):
        return model_changelist_url_to_html(
            app="courses",
            model="requisite",
            query_key="course_from__id",
            query_val=instance.id,
            placeholder=instance.requisites_from.count(),
        )

    @admin.display(ordering="requisites_to_count", description=_("Number of Requisities-To"))
    def requisites_to_count(self, instance: Course):
        return model_changelist_url_to_html(
            app="courses",
            model="requisite",
            query_key="course_to__id",
            query_val=instance.id,
            placeholder=instance.requisites_to.count(),
        )

    @admin.display(ordering="classrooms_count", description=_("Number of Classrooms"))
    def classrooms_count(self, instance: Course):
        return model_changelist_url_to_html(
            app="classrooms",
            model="classroom",
            query_key="course__id",
            query_val=instance.id,
            placeholder=instance.classrooms.count(),
        )

    @admin.display(ordering="references_count", description=_("Number of References"))
    def references_count(self, instance: Course):
        return model_changelist_url_to_html(
            app="references",
            model="reference",
            query_key="courses_id",
            query_val=instance.id,
            placeholder=instance.references.count(),
        )

    @admin.display(ordering="resources_count", description=_("Number of Resources"))
    def resources_count(self, instance: Course):
        return model_changelist_url_to_html(
            app="resources",
            model="resource",
            query_key="classroom__course__id",
            query_val=instance.id,
            placeholder=instance.resources_count,
        )
    
    @admin.display(ordering="recordings_count", description=_("Number of Recordings"))
    def recordings_count(self, instance: Course):
        return model_changelist_url_to_html(
            app="recordings",
            model="recordedclassroom",
            query_key="classroom__course__id",
            query_val=instance.id,
            placeholder=instance.recordings_count,
        )

    def get_queryset(self, request):
        return super().get_queryset(request) \
            .annotate(
                resources_count=Count("classrooms__resources", distinct=True),
                recordings_count=Count("classrooms__recordings", distinct=True),
            ).prefetch_related(
                "requisites_from",
                "requisites_to",
                "classrooms",
                "references",
            )


@admin.register(Requisite)
class RequisiteAdmin(admin.ModelAdmin):
    autocomplete_fields = ("course_from", "course_to",)
    list_per_page = 25
    list_display = ("id", "course_from_", "course_to_", "type",)
    list_select_related = ("course_from", "course_to",)
    search_fields = ("course_from__title", "course_to__title",
                     "course_from__en_title", "course_to__en_title")
    list_filter = ("type",)

    @admin.display(description=_("Course From"))
    def course_from_(self, instance: Course):
        return model_change_url_to_html(
            app="courses",
            model="course",
            args=(instance.course_from.id,),
            placeholder=instance.course_from,
        )

    @admin.display(description=_("Course To"))
    def course_to_(self, instance: Course):
        return model_change_url_to_html(
            app="courses",
            model="course",
            args=(instance.course_to.id,),
            placeholder=instance.course_to,
        )
