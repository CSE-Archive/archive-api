from .models import Course, TA, Resource, Requisite, Classroom
from reference.models import ReferenceItem
from teacher.models import TeacherItem
from jdatetime import datetime as jdt
from django.urls import reverse
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Count, OuterRef, Subquery
from django.utils.html import format_html, urlencode
from django.utils.timezone import localtime
from django.utils.translation import gettext as _


class TeacherItemInline(GenericTabularInline):
    autocomplete_fields = ("teacher",)
    model = TeacherItem
    extra = 0


class ReferenceItemInline(GenericTabularInline):
    autocomplete_fields = ("reference",)
    model = ReferenceItem
    extra = 0


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
    inlines = (ReferenceItemInline, RequisiteFromInline, RequisiteToInline,)
    list_per_page = 10
    list_display = ("id", "title", "en_title", "unit", "type", "references_count",
                    "classrooms_count", "resources_count", "requisites_from_count",
                    "requisites_to_count",)
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
        placeholder = course.classrooms_count if course.classrooms_count else "0"
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

    @admin.display(ordering="references_count", description=_("تعداد مراجع"))
    def references_count(self, course):
        url = (
            reverse("admin:reference_referenceitem_changelist")
            + "?"
            + urlencode({
                "object_id": str(course.id)
            })
        )
        placeholder = course.references_count if course.references_count else "0"
        return format_html('<a href="{}">{}</a>', url, placeholder)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            resources_count=Count("classrooms__resources"),
            classrooms_count=Subquery(
                Classroom.objects.filter(course=OuterRef("pk"))
                .values("course_id").annotate(count=Count("id")).values("count")),
            requisites_from_count=Subquery(
                Requisite.objects.filter(course_from=OuterRef("pk"))
                .values("course_from_id").annotate(count=Count("id")).values("count")),
            requisites_to_count=Subquery(
                Requisite.objects.filter(course_to=OuterRef("pk"))
                .values("course_to_id").annotate(count=Count("id")).values("count")),
            references_count=Subquery(
                ReferenceItem.objects.filter(object_id=OuterRef("pk"))
                .values("object_id").annotate(count=Count("id")).values("count")),
        )


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    inlines = (TeacherItemInline, TAInline, ResourceInline,)
    autocomplete_fields = ("course",)
    list_per_page = 10
    list_display = ("id", "year", "semester", "course",
                    "tas_count", "resources_count", "teachers_count",)
    list_select_related = ("course",)
    list_filter = ("year", "semester", "course",)
    search_fields = ("year", "semester", "course__title", "course__en_title",)

    @admin.display(ordering="tas_count", description=_("تعداد گریدرها"))
    def tas_count(self, classroom):
        url = (
            reverse("admin:course_ta_changelist")
            + "?"
            + urlencode({
                "classroom__id": str(classroom.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, classroom.tas_count)

    @admin.display(ordering="resources_count", description=_("تعداد منابع"))
    def resources_count(self, classroom):
        url = (
            reverse("admin:course_resource_changelist")
            + "?"
            + urlencode({
                "classroom__id": str(classroom.id)
            })
        )
        placeholder = classroom.resources_count if classroom.resources_count else "0"
        return format_html('<a href="{}">{}</a>', url, placeholder)

    @admin.display(ordering="teachers_count", description=_("تعداد اساتید"))
    def teachers_count(self, classroom):
        url = (
            reverse("admin:teacher_teacheritem_changelist")
            + "?"
            + urlencode({
                "object_id": str(classroom.id)
            })
        )
        placeholder = classroom.teachers_count if classroom.teachers_count else "0"
        return format_html('<a href="{}">{}</a>', url, placeholder)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            tas_count=Count("tas"),
            resources_count=Subquery(
                Resource.objects.filter(classroom=OuterRef("pk"))
                .values("classroom_id").annotate(count=Count("id")).values("count")),
            teachers_count=Subquery(
                TeacherItem.objects.filter(object_id=OuterRef("pk"))
                .values("object_id").annotate(count=Count("id")).values("count")),
        )


@admin.register(TA)
class TAAdmin(admin.ModelAdmin):
    autocomplete_fields = ("classroom",)
    list_per_page = 10
    list_display = ("id", "full_name", "classroom", "course",)
    list_select_related = ("classroom__course",)
    list_filter = ("classroom", "classroom__course",)
    search_fields = ("full_name",)

    @admin.display(ordering="course", description=_("درس"))
    def course(self, ta):
        return ta.classroom.course


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
