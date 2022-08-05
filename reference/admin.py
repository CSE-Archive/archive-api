from .models import Author, Reference
from course.models import Course
from jdatetime import datetime as jdt
from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html, urlencode
from django.utils.timezone import localtime
from django.utils.translation import gettext as _


class AuthorInline(admin.TabularInline):
    model = Author
    extra = 0


class CourseInline(admin.TabularInline):
    model = Course.references.through
    extra = 0
    autocomplete_fields = ("course",)
    verbose_name = "درس"
    verbose_name_plural = "دروس"


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    inlines = (AuthorInline, CourseInline,)
    list_per_page = 10
    list_display = ("id", "cover_image_", "title", "authors_count", "date_modified_",
                    "date_created_", "courses_count",)
    readonly_fields = ("preview",)
    list_filter = ("date_modified", "date_created",)
    search_fields = ("title", "authors__full_name",)

    @admin.display(description=_("پیش‌نمایش تصویر جلد"))
    def preview(self, reference):
        if reference.cover_image.name != "":
            return format_html(f'<img src="{reference.cover_image.url}" width="500" style="object-fit:contain;"/>')
        return ""

    @admin.display(description=_("تصویر جلد"))
    def cover_image_(self, reference):
        if reference.cover_image.name != "":
            url = reference.cover_image.url
            return format_html(f'<a href="{url}"><img src="{url}" width="100" height="100" style="object-fit:cover;"/></a>')
        return ""

    @admin.display(ordering="authors_count", description=_("تعداد نویسنده‌ها"))
    def authors_count(self, reference):
        return reference.authors.count()
    
    @admin.display(ordering="courses_count", description=_("تعداد درس‌ها"))
    def courses_count(self, reference):
        url = (
            reverse("admin:course_course_changelist")
            + "?"
            + urlencode({
                "references": str(reference.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, reference.courses.count())

    @admin.display(ordering="date_created", description=_("تاریخ اضافه شدن"))
    def date_created_(self, reference):
        return jdt.fromgregorian(
            date=localtime(reference.date_created)
        ).strftime("%Y-%m-%d %H:%M:%S")

    @admin.display(ordering="date_modified", description=_("آخرین ویرایش"))
    def date_modified_(self, reference):
        return jdt.fromgregorian(
            date=localtime(reference.date_modified)
        ).strftime("%Y-%m-%d %H:%M:%S")

    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related("authors",)
