from .models import Email, ExternalLink, Teacher, TeacherItem
from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html, urlencode
from django.utils.translation import gettext as _
from django.db.models import F, Value, Count, OuterRef, Subquery
from django.db.models.functions import Concat


class EmailInline(admin.TabularInline):
    model = Email
    extra = 0


class ExternalLinkInline(admin.TabularInline):
    model = ExternalLink
    extra = 0


class TeacherItemInline(admin.TabularInline):
    model = TeacherItem
    extra = 0


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    inlines = (EmailInline, ExternalLinkInline, TeacherItemInline,)
    list_per_page = 10
    list_display = ("id", "image_", "full_name", "department",
                    "emails_count", "external_links_count",)
    readonly_fields = ("preview",)
    list_filter = ("department",)
    search_fields = ("first_name", "last_name", "about",)

    @admin.display(description=_("تصویر"))
    def image_(self, teacher):
        if teacher.image.name != "":
            url = teacher.image.url
            return format_html(f'<a href="{url}"><img src="{url}" width="100" height="100" style="object-fit:cover;"/></a>')
        return ""

    @admin.display(description=_("پیش‌نمایش تصویر"))
    def preview(self, teacher):
        if teacher.image.name != "":
            return format_html(f'<img src="{teacher.image.url}" width="500" style="object-fit:contain;"/>')
        return ""

    @admin.display(ordering="full_name", description=_("نام و نام خانوادگی"))
    def full_name(self, teacher):
        return teacher.full_name

    @admin.display(ordering="emails_count", description=_("تعداد ایمیل‌ها"))
    def emails_count(self, teacher):
        url = (
            reverse("admin:teacher_email_changelist")
            + "?"
            + urlencode({
                "teacher__id": str(teacher.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, teacher.emails_count)

    @admin.display(ordering="external_links_count", description=_("تعداد لینک‌ها"))
    def external_links_count(self, teacher):
        url = (
            reverse("admin:teacher_externallink_changelist")
            + "?"
            + urlencode({
                "teacher__id": str(teacher.id)
            })
        )
        placeholder = teacher.external_links_count if teacher.external_links_count else "0"
        return format_html('<a href="{}">{}</a>', url, placeholder)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            full_name=Concat(F("first_name"), Value(" "), F("last_name")),
            emails_count=Count("emails"),
            external_links_count=Subquery(
                ExternalLink.objects.filter(teacher=OuterRef("pk"))
                .values("teacher_id").annotate(count=Count("id")).values("count")),
        )


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    autocomplete_fields = ("teacher",)
    list_per_page = 10
    list_display = ("id", "email", "teacher")
    list_filter = ("teacher",)
    search_fields = ("email",)


@admin.register(ExternalLink)
class ExternalLinkAdmin(admin.ModelAdmin):
    autocomplete_fields = ("teacher",)
    list_per_page = 10
    list_display = ("id", "url", "teacher")
    list_filter = ("teacher",)
    search_fields = ("url",)


@admin.register(TeacherItem)
class TeacherItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ("teacher",)
    list_per_page = 10
    list_display = ("id", "teacher_", "content_object_",)
    list_select_related = ("teacher",)
    list_filter = ("teacher",)

    @admin.display(ordering="teacher_", description=_("استاد"))
    def teacher_(self, teacher_item):
        url = (
            reverse("admin:teacher_teacher_changelist")
            + str(teacher_item.teacher.id)
            + "/"
            + "change"
        )
        return format_html('<a href="{}">{}</a>', url, f"{teacher_item.teacher.first_name} {teacher_item.teacher.last_name}")

    @admin.display(ordering="content_object_", description=_("محتوای مربوطه"))
    def content_object_(self, teacher_item):
        return teacher_item.content_object

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("content_object")
