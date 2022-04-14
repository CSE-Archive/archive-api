import jdatetime

from . import models
from django.urls import reverse
from django.contrib import admin
from django.db.models import Count, OuterRef, Subquery
from django.utils.html import format_html, urlencode
from django.utils.timezone import localtime
from django.utils.translation import gettext as _


class RequisiteFromInline(admin.TabularInline):
    fk_name = "course_from"
    model = models.Requisite
    autocomplete_fields = ("course_to",)
    extra = 0


class RequisiteToInline(admin.TabularInline):
    fk_name = "course_to"
    model = models.Requisite
    autocomplete_fields = ("course_from",)
    extra = 0


class TAInline(admin.TabularInline):
    model = models.TA
    extra = 0


class ResourceInline(admin.TabularInline):
    model = models.Resource
    extra = 0


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = (RequisiteFromInline, RequisiteToInline,)
    list_per_page = 10
    list_display = ("id", "title", "en_title", "unit", "term_in_chart", "type",
                    "sessionses_count", "resources_count", "requisites_from_count",
                    "requisites_to_count",)
    search_fields = ("title", "en_title",)
    list_filter = ("type", "unit", "term_in_chart",)
    fields = (
        ("title", "unit",),
        ("en_title", "term_in_chart",),
        "type",
        "tag",
        "description",
    )

    @admin.display(ordering="resources_count", description=_("تعداد منابع"))
    def resources_count(self, course):
        url = (
            reverse("admin:course_resource_changelist")
            + "?"
            + urlencode({
                "session__course__id": str(course.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, course.resources_count)

    @admin.display(ordering="sessionses_count", description=_("تعداد کلاس‌ها"))
    def sessionses_count(self, course):
        url = (
            reverse("admin:course_session_changelist")
            + "?"
            + urlencode({
                "course__id": str(course.id)
            })
        )
        placeholder = course.sessionses_count if course.sessionses_count else "0"
        return format_html('<a href="{}">{}</a>', url, placeholder)

    @admin.display(ordering="requisites_from_count", description=_("تعداد نیازهای مبدا"))
    def requisites_from_count(self, course):
        url = (
            reverse("admin:course_requisite_changelist")
            + "?"
            + urlencode({
                "course_from__id": str(course.id)
            })
        )
        placeholder = course.requisites_from_count if course.requisites_from_count else "0"
        return format_html('<a href="{}">{}</a>', url, placeholder)

    @admin.display(ordering="requisites_to_count", description=_("تعداد نیازهای مقصد"))
    def requisites_to_count(self, course):
        url = (
            reverse("admin:course_requisite_changelist")
            + "?"
            + urlencode({
                "course_to__id": str(course.id)
            })
        )
        placeholder = course.requisites_to_count if course.requisites_to_count else "0"
        return format_html('<a href="{}">{}</a>', url, placeholder)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            resources_count=Count("session__resource"),
            sessionses_count=Subquery(
                models.Session.objects.filter(course=OuterRef("pk"))
                .values("course_id").annotate(count=Count("id")).values("count")),
            requisites_from_count=Subquery(
                models.Requisite.objects.filter(course_from=OuterRef("pk"))
                .values("course_from_id").annotate(count=Count("id")).values("count")),
            requisites_to_count=Subquery(
                models.Requisite.objects.filter(course_to=OuterRef("pk"))
                .values("course_to_id").annotate(count=Count("id")).values("count")),
        )


@admin.register(models.Session)
class SessionAdmin(admin.ModelAdmin):
    inlines = (TAInline, ResourceInline,)
    autocomplete_fields = ("course",)
    list_per_page = 10
    list_display = ("id", "year", "semester", "course",
                    "resources_count", "tas_count",)
    list_select_related = ("course",)
    list_filter = ("year", "semester", "course",)
    search_fields = ("year", "semester", "course__title", "course__en_title",)

    @admin.display(ordering="tas_count", description=_("تعداد گریدرها"))
    def tas_count(self, session):
        url = (
            reverse("admin:course_ta_changelist")
            + "?"
            + urlencode({
                "session__id": str(session.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, session.tas_count)

    @admin.display(ordering="resources_count", description=_("تعداد منابع"))
    def resources_count(self, session):
        url = (
            reverse("admin:course_resource_changelist")
            + "?"
            + urlencode({
                "session__id": str(session.id)
            })
        )
        placeholder = session.resources_count if session.resources_count else "0"
        return format_html('<a href="{}">{}</a>', url, placeholder)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            tas_count=Count("ta"),
            resources_count=Subquery(
                models.Resource.objects.filter(session=OuterRef("pk"))
                .values("session_id").annotate(count=Count("id")).values("count")),
        )


@admin.register(models.TA)
class TAAdmin(admin.ModelAdmin):
    autocomplete_fields = ("session",)
    list_per_page = 10
    list_display = ("id", "full_name", "session", "course",)
    list_select_related = ("session__course",)
    list_filter = ("session", "session__course",)
    search_fields = ("full_name",)

    @admin.display(ordering="course", description=_("درس"))
    def course(self, ta):
        return ta.session.course


@admin.register(models.Resource)
class ResourceAdmin(admin.ModelAdmin):
    autocomplete_fields = ("session",)
    list_per_page = 10
    list_display = ("id", "title", "type", "date_modified_",
                    "date_created_", "session", "course",)
    list_select_related = ("session__course",)
    list_filter = ("date_modified", "date_created", "session",
                   "session__course", "type",)
    search_fields = ("title",)

    @admin.display(ordering="course", description=_("درس"))
    def course(self, resource):
        return resource.session.course
    
    @admin.display(ordering="date_created", description=_("تاریخ اضافه شدن"))
    def date_created_(self, resource):
        return jdatetime.datetime.fromgregorian(
            date=localtime(resource.date_created)
        ).strftime("%Y-%m-%d %H:%M:%S")

    @admin.display(ordering="date_modified", description=_("آخرین ویرایش"))
    def date_modified_(self, resource):
        return jdatetime.datetime.fromgregorian(
            date=localtime(resource.date_modified)
        ).strftime("%Y-%m-%d %H:%M:%S")


@admin.register(models.Requisite)
class RequisiteAdmin(admin.ModelAdmin):
    autocomplete_fields = ("course_from", "course_to",)
    list_per_page = 10
    list_display = ("id", "course_from", "course_to", "type",)
    search_fields = ("course_from__title", "course_to__title",
                     "course_from__en_title", "course_to__en_title")
    list_filter = ("type",)
