from .models import Course, TA, Resource, Requisite, Classroom
from jdatetime import datetime as jdt
from django.urls import reverse
from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.utils.timezone import localtime
from django.utils.translation import gettext as _


class RequisiteFromInline(admin.TabularInline):
    fk_name = "course_from"
    model = Requisite
    autocomplete_fields = ("course_to",)
    extra = 0


class RequisiteToInline(admin.TabularInline):
    fk_name = "course_to"
    model = Requisite
    autocomplete_fields = ("course_from",)
    extra = 0


class TAInline(admin.TabularInline):
    model = TA
    extra = 0


class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = (RequisiteFromInline, RequisiteToInline,)
    list_per_page = 10
    list_display = ("id", "title", "en_title", "unit", "type",
                    "classrooms_count", "resources_count", "requisites_from_count",
                    "requisites_to_count", "references_count",)
    search_fields = ("title", "en_title", "description", "tag",)
    list_filter = ("type", "unit",)

    @admin.display(ordering="resources_count", description=_("تعداد منابع"))
    def resources_count(self, course):
        url = (
            reverse("admin:course_resource_changelist")
            + "?"
            + urlencode({
                "classroom__course__id": str(course.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, course.resources_count)

    @admin.display(ordering="classrooms_count", description=_("تعداد کلاس‌ها"))
    def classrooms_count(self, course):
        url = (
            reverse("admin:course_classroom_changelist")
            + "?"
            + urlencode({
                "course__id": str(course.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, course.classrooms.count())

    @admin.display(ordering="requisites_from_count", description=_("تعداد نیازهای مبدا"))
    def requisites_from_count(self, course):
        url = (
            reverse("admin:course_requisite_changelist")
            + "?"
            + urlencode({
                "course_from__id": str(course.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, course.requisites_from.count())

    @admin.display(ordering="requisites_to_count", description=_("تعداد نیازهای مقصد"))
    def requisites_to_count(self, course):
        url = (
            reverse("admin:course_requisite_changelist")
            + "?"
            + urlencode({
                "course_to__id": str(course.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, course.requisites_to.count())

    @admin.display(ordering="references_count", description=_("تعداد مراجع"))
    def references_count(self, course):
        url = (
            reverse("admin:reference_reference_changelist")
            + "?"
            + urlencode({
                "courses_id": str(course.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, course.references.count())

    def get_queryset(self, request):
        return super().get_queryset(request) \
            .annotate(resources_count=Count("classrooms__resources")) \
            .prefetch_related(
                "classrooms",
                "requisites_from",
                "requisites_to",
                "references",
            )


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    inlines = (TAInline, ResourceInline,)
    autocomplete_fields = ("course",)
    list_per_page = 10
    list_display = ("id", "year", "semester", "course",
                    "tas_count", "resources_count", "teachers_count",)
    list_select_related = ("course",)
    list_filter = ("year", "semester", "course",)
    search_fields = ("year", "semester", "course__title",
                    "course__en_title", "tas__full_name",
                    "teachers__last_name",)

    @admin.display(ordering="tas_count", description=_("تعداد گریدرها"))
    def tas_count(self, classroom):
        return classroom.tas.count()

    @admin.display(ordering="resources_count", description=_("تعداد منابع"))
    def resources_count(self, classroom):
        url = (
            reverse("admin:course_resource_changelist")
            + "?"
            + urlencode({
                "classroom__id": str(classroom.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, classroom.resources.count())

    @admin.display(ordering="teachers_count", description=_("تعداد اساتید"))
    def teachers_count(self, classroom):
        url = (
            reverse("admin:teacher_teacher_changelist")
            + "?"
            + urlencode({
                "classrooms": str(classroom.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, classroom.teachers.count())

    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related(
                "tas",
                "resources",
                "teachers",
            )


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    autocomplete_fields = ("classroom",)
    list_per_page = 10
    list_display = ("id", "title", "type", "date_modified_",
                    "date_created_", "classroom", "course",)
    list_select_related = ("classroom__course",)
    list_filter = ("date_modified", "date_created", "type", "classroom",
                   "classroom__course",)
    search_fields = ("title",)

    @admin.display(ordering="course", description=_("درس"))
    def course(self, resource):
        return resource.classroom.course

    @admin.display(ordering="date_created", description=_("تاریخ اضافه شدن"))
    def date_created_(self, resource):
        return jdt.fromgregorian(
            date=localtime(resource.date_created)
        ).strftime("%Y-%m-%d %H:%M:%S")

    @admin.display(ordering="date_modified", description=_("آخرین ویرایش"))
    def date_modified_(self, resource):
        return jdt.fromgregorian(
            date=localtime(resource.date_modified)
        ).strftime("%Y-%m-%d %H:%M:%S")


@admin.register(Requisite)
class RequisiteAdmin(admin.ModelAdmin):
    autocomplete_fields = ("course_from", "course_to",)
    list_per_page = 10
    list_display = ("id", "course_from", "course_to", "type",)
    search_fields = ("course_from__title", "course_to__title",
                     "course_from__en_title", "course_to__en_title")
    list_filter = ("type",)
