from . import models
from django.contrib import admin
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.urls import reverse
from django.db.models import Count, OuterRef, Subquery
from django.utils.html import format_html, urlencode


class EmailInline(admin.TabularInline):
    model = models.Email
    extra = 0


class ExternalLinkInline(admin.TabularInline):
    model = models.ExternalLink
    extra = 0


@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    inlines = (EmailInline, ExternalLinkInline,)
    list_per_page = 10
    list_display = ("id", "full_name", "image",
                    "emails_count", "external_links_count",)
    search_fields = ("full_name",)

    @admin.display(ordering="full_name")
    def full_name(self, teacher):
        return teacher.full_name

    @admin.display(ordering="emails_count")
    def emails_count(self, teacher):
        url = (
            reverse("admin:teacher_email_changelist")
            + "?"
            + urlencode({
                "teacher__id": str(teacher.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, teacher.emails_count)

    @admin.display(ordering="external_links_count")
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
            emails_count=Count("email"),
            external_links_count=Subquery(
                models.ExternalLink.objects.filter(teacher=OuterRef("pk"))
                .values("teacher_id").annotate(count=Count("id")).values("count")),
        )


@admin.register(models.Email)
class EmailAdmin(admin.ModelAdmin):
    autocomplete_fields = ("teacher",)
    list_per_page = 10
    list_display = ("id", "email", "teacher")
    list_filter = ("teacher",)
    search_fields = ("email",)


@admin.register(models.ExternalLink)
class ExternalLinkAdmin(admin.ModelAdmin):
    autocomplete_fields = ("teacher",)
    list_per_page = 10
    list_display = ("id", "url", "teacher")
    list_filter = ("teacher",)
    search_fields = ("url",)


@admin.register(models.TeacherItem)
class TeacherItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ("teacher",)
    list_per_page = 10
    list_display = ("id", "teacher_", "content_object",)
    list_filter = ("teacher",)

    @admin.display(ordering="teacher_")
    def teacher_(self, teacher_item):
        url = (
            reverse("admin:teacher_teacher_changelist")
            + str(teacher_item.teacher.id)
            + "/"
            + "change"
        )
        return format_html('<a href="{}">{}</a>', url, f"{teacher_item.teacher.first_name} {teacher_item.teacher.last_name}")
