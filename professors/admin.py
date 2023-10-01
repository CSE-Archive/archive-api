from django.contrib import admin
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
import nested_admin

from core.admin import BaseAdminMixin, LinkNestedInlineAdmin
from core.helpers import image_url_to_html, model_changelist_url_to_html
from classrooms.models import Classroom
from professors.models import Department, Professor, Email


class EmailInlineAdmin(nested_admin.NestedTabularInline):
    model = Email
    extra = 0
    verbose_name = _("Email")
    verbose_name_plural = _("Emails")


class ClassroomInlineAdmin(nested_admin.NestedTabularInline):
    model = Classroom.professors.through
    extra = 0
    autocomplete_fields = ("classroom",)
    verbose_name = _("Classroom")
    verbose_name_plural = _("Classrooms")


@admin.register(Professor)
class ProfessorAdmin(BaseAdminMixin, nested_admin.NestedModelAdmin):
    inlines = (EmailInlineAdmin, LinkNestedInlineAdmin, ClassroomInlineAdmin,)
    list_per_page = 25
    list_display = ("uuid", "image_", "full_name", "department",
                    "emails_count", "links_count", "classrooms_count")
    list_select_related = ("department",)
    readonly_fields = ("preview",)
    list_filter = ("department",)
    search_fields = ("uuid", "first_name", "last_name", "about",
                    "emails__address", "links__url",)

    @admin.display(description=_("Preview Image"))
    def preview(self, instance: Professor):
        return image_url_to_html(
            image=instance.image,
            style="contain",
            height=100,
            open_in_new_tab=True,
        )

    @admin.display(description=_("Image"))
    def image_(self, instance: Professor):
        return image_url_to_html(
            image=instance.image,
            style="cover",
            height=100,
            open_in_new_tab=True,
        )

    @admin.display(ordering="full_name", description=_("Full Name"))
    def full_name(self, instance: Professor):
        return f"{instance.honorific} {instance.first_name} {instance.last_name}"

    @admin.display(ordering="emails_count", description=_("Number of Emails"))
    def emails_count(self, instance: Professor):
        return instance.emails.count()

    @admin.display(ordering="links_count", description=_("Number of Links"))
    def links_count(self, instance: Professor):
        return instance.links.count()
    
    @admin.display(ordering="classrooms_count", description=_("Number of Classrooms"))
    def classrooms_count(self, instance: Professor):
        return model_changelist_url_to_html(
            app="classrooms",
            model="classroom",
            query_key="professors",
            query_val=instance.id,
            placeholder=instance.classrooms.count(),
        )

    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related(
                "emails",
                "links",
                "classrooms",
            )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_per_page = 25
    list_display = ("uuid", "name", "name_en", "professors_count",)
    search_fields = ("uuid", "name", "name_en",)

    @admin.display(ordering="professors_count", description=_("Number of Professors"))
    def professors_count(self, instance: Department):
        return model_changelist_url_to_html(
            app="professors",
            model="professor",
            query_key="department",
            query_val=instance.id,
            placeholder=instance.professors_count,
        )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            professors_count=Count("professors", distinct=True),
        )
