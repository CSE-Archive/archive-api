from .models import Email, ExternalLink, Teacher
from course.models import Classroom
from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html, urlencode
from django.utils.translation import gettext as _


class EmailInline(admin.TabularInline):
    model = Email
    extra = 0


class ExternalLinkInline(admin.TabularInline):
    model = ExternalLink
    extra = 0


class ClassroomInline(admin.TabularInline):
    model = Classroom.teachers.through
    extra = 0
    autocomplete_fields = ("classroom",)
    verbose_name = "کلاس"
    verbose_name_plural = "کلاس‌ها"


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    inlines = (EmailInline, ExternalLinkInline, ClassroomInline,)
    list_per_page = 10
    list_display = ("id", "image_", "full_name", "department",
                    "emails_count", "external_links_count", "classrooms_count")
    readonly_fields = ("preview",)
    list_filter = ("department",)
    search_fields = ("first_name", "last_name", "about",
                    "emails__email", "external_links__url",)

    @admin.display(description=_("پیش‌نمایش تصویر"))
    def preview(self, teacher):
        if teacher.image.name != "":
            return format_html(f'<img src="{teacher.image.url}" width="500" style="object-fit:contain;"/>')
        return ""

    @admin.display(description=_("تصویر"))
    def image_(self, teacher):
        if teacher.image.name != "":
            url = teacher.image.url
            return format_html(f'<a href="{url}"><img src="{url}" width="100" height="100" style="object-fit:cover;"/></a>')
        return ""

    @admin.display(ordering="full_name", description=_("نام و نام خانوادگی"))
    def full_name(self, teacher):
        return f"{teacher.first_name} {teacher.last_name}"

    @admin.display(ordering="emails_count", description=_("تعداد ایمیل‌ها"))
    def emails_count(self, teacher):
        return teacher.emails.count()

    @admin.display(ordering="external_links_count", description=_("تعداد لینک‌ها"))
    def external_links_count(self, teacher):
        return teacher.external_links.count()
    
    @admin.display(ordering="classrooms_count", description=_("تعداد کلاس‌ها"))
    def classrooms_count(self, teacher):
        url = (
            reverse("admin:course_classroom_changelist")
            + "?"
            + urlencode({
                "teachers": str(teacher.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, teacher.classrooms.count())

    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related(
                "emails",
                "external_links",
                "classrooms",
            )
