from . import models
from django.urls import reverse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count, OuterRef, Subquery
from django.utils.html import format_html, urlencode
from django.utils.translation import gettext as _
from django.contrib.contenttypes.admin import GenericTabularInline
from course.admin import CourseAdmin, SessionAdmin
from course.models import Course, Session
from teacher.models import TeacherItem
from reference.models import ReferenceItem


class TeacherItemInline(GenericTabularInline):
    autocomplete_fields = ("teacher",)
    model = TeacherItem
    extra = 0


class ReferenceItemInline(GenericTabularInline):
    autocomplete_fields = ("reference",)
    model = ReferenceItem
    extra = 0


class CustomSessionAdmin(SessionAdmin):
    inlines = (TeacherItemInline,) + SessionAdmin.inlines
    list_display = SessionAdmin.list_display + ("teachers_count",)

    @admin.display(ordering="teachers_count", description=_("تعداد اساتید"))
    def teachers_count(self, session):
        url = (
            reverse("admin:teacher_teacheritem_changelist")
            + "?"
            + urlencode({
                "object_id": str(session.id)
            })
        )
        placeholder = session.teachers_count if session.teachers_count else "0"
        return format_html('<a href="{}">{}</a>', url, placeholder)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            teachers_count=Subquery(
                TeacherItem.objects.filter(object_id=OuterRef("pk"))
                .values("object_id").annotate(count=Count("id")).values("count")),
        )


class CustomCourseAdmin(CourseAdmin):
    inlines = (ReferenceItemInline,) + CourseAdmin.inlines
    list_display = CourseAdmin.list_display + ("references_count",)

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
            references_count=Subquery(
                ReferenceItem.objects.filter(object_id=OuterRef("pk"))
                .values("object_id").annotate(count=Count("id")).values("count")),
        )


admin.site.unregister(Session)
admin.site.register(Session, CustomSessionAdmin)

admin.site.unregister(Course)
admin.site.register(Course, CustomCourseAdmin)


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )
