from .models import Course, TA, Resource, Requisite, Classroom
from core.helpers import gregorian_to_jalali, model_changelist_url_to_html
from django.contrib import admin
from django.db.models import Count
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


class ClassroomInline(admin.TabularInline):
    model = Classroom.tas.through
    extra = 0
    autocomplete_fields = ("classroom",)
    verbose_name = "کلاس"
    verbose_name_plural = "کلاس‌ها"


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
        return model_changelist_url_to_html(
            app="course",
            model="resource",
            query_key="classroom__course__id",
            query_val=course.id,
            placeholder=course.resources_count,
        )

    @admin.display(ordering="classrooms_count", description=_("تعداد کلاس‌ها"))
    def classrooms_count(self, course):
        return model_changelist_url_to_html(
            app="course",
            model="classroom",
            query_key="course__id",
            query_val=course.id,
            placeholder=course.classrooms.count(),
        )

    @admin.display(ordering="requisites_from_count", description=_("تعداد نیازهای مبدا"))
    def requisites_from_count(self, course):
        return model_changelist_url_to_html(
            app="course",
            model="requisite",
            query_key="course_from__id",
            query_val=course.id,
            placeholder=course.requisites_from.count(),
        )

    @admin.display(ordering="requisites_to_count", description=_("تعداد نیازهای مقصد"))
    def requisites_to_count(self, course):
        return model_changelist_url_to_html(
            app="course",
            model="requisite",
            query_key="course_to__id",
            query_val=course.id,
            placeholder=course.requisites_to.count(),
        )

    @admin.display(ordering="references_count", description=_("تعداد مراجع"))
    def references_count(self, course):
        return model_changelist_url_to_html(
            app="reference",
            model="reference",
            query_key="courses_id",
            query_val=course.id,
            placeholder=course.references.count(),
        )

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
    inlines = (ResourceInline,)
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
        return model_changelist_url_to_html(
            app="course",
            model="ta",
            query_key="classrooms",
            query_val=classroom.id,
            placeholder=classroom.tas.count(),
        )

    @admin.display(ordering="resources_count", description=_("تعداد منابع"))
    def resources_count(self, classroom):
        return model_changelist_url_to_html(
            app="course",
            model="resource",
            query_key="classroom__id",
            query_val=classroom.id,
            placeholder=classroom.resources.count(),
        )

    @admin.display(ordering="teachers_count", description=_("تعداد اساتید"))
    def teachers_count(self, classroom):
        return model_changelist_url_to_html(
            app="teacher",
            model="teacher",
            query_key="classrooms",
            query_val=classroom.id,
            placeholder=classroom.teachers.count(),
        )

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
        return gregorian_to_jalali(resource.date_created)

    @admin.display(ordering="date_modified", description=_("آخرین ویرایش"))
    def date_modified_(self, resource):
        return gregorian_to_jalali(resource.date_modified)


@admin.register(Requisite)
class RequisiteAdmin(admin.ModelAdmin):
    autocomplete_fields = ("course_from", "course_to",)
    list_per_page = 10
    list_display = ("id", "course_from", "course_to", "type",)
    search_fields = ("course_from__title", "course_to__title",
                     "course_from__en_title", "course_to__en_title")
    list_filter = ("type",)


@admin.register(TA)
class TAAdmin(admin.ModelAdmin):
    inlines = (ClassroomInline,)
    list_per_page = 10
    list_display = ("id", "full_name", "classroom_count",)
    search_fields = ("full_name",)

    @admin.display(ordering="classroom_count", description=_("تعداد کلاس‌ها"))
    def classroom_count(self, ta):
        return model_changelist_url_to_html(
            app="course",
            model="classroom",
            query_key="tas",
            query_val=ta.id,
            placeholder=ta.classrooms.count(),
        )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            "classrooms",
        )
