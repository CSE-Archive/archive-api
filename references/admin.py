from django.contrib import admin
from django.utils.translation import gettext_lazy as _
import nested_admin

from core.admin import BaseAdminMixin, LinkNestedInlineAdmin
from core.helpers import image_url_to_html, gregorian_to_jalali, model_changelist_url_to_html
from references.models import Writer, Reference


class ReferenceNestedInlineAdmin(nested_admin.NestedTabularInline):
    model = Reference.writers.through
    extra = 0
    autocomplete_fields = ("reference",)
    verbose_name = _("Reference")
    verbose_name_plural = _("References")


@admin.register(Reference)
class ReferenceAdmin(BaseAdminMixin, nested_admin.NestedModelAdmin):
    inlines = (LinkNestedInlineAdmin,)
    list_per_page = 25
    list_display = ("uuid", "cover_image_", "title", "type", "writers_count",
                    "courses_count", "modified_time_", "created_time_",)
    readonly_fields = ("preview",)
    list_filter = ("modified_time", "created_time", "type", "courses__id",)
    search_fields = ("uuid", "title", "writers__full_name",)

    @admin.display(description=_("Cover Image Preview"))
    def preview(self, instance: Reference):
        return image_url_to_html(
            image=instance.cover_image,
            style="contain",
            height=100,
            open_in_new_tab=True,
        )

    @admin.display(description=_("Cover Image"))
    def cover_image_(self, instance: Reference):
        return image_url_to_html(
            image=instance.cover_image,
            style="cover",
            height=100,
            open_in_new_tab=True,
        )

    @admin.display(ordering="writers_count", description=_("Number of Writers"))
    def writers_count(self, instance: Reference):
        return model_changelist_url_to_html(
            app="references",
            model="writer",
            query_key="references",
            query_val=instance.id,
            placeholder=instance.writers.count(),
        )
    
    @admin.display(ordering="courses_count", description=_("Number of Courses"))
    def courses_count(self, instance: Reference):
        return model_changelist_url_to_html(
            app="courses",
            model="course",
            query_key="references",
            query_val=instance.id,
            placeholder=instance.courses.count(),
        )

    @admin.display(ordering="created_time", description=_("Created Time"))
    def created_time_(self, instance: Reference):
        return gregorian_to_jalali(instance.created_time)

    @admin.display(ordering="modified_time", description=_("Modified Time"))
    def modified_time_(self, instance: Reference):
        return gregorian_to_jalali(instance.modified_time)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            "writers",
            "courses",
        )


@admin.register(Writer)
class WriterAdmin(nested_admin.NestedModelAdmin):
    inlines = (ReferenceNestedInlineAdmin,)
    list_per_page = 25
    list_display = ("id", "full_name", "references_count",)
    search_fields = ("full_name",)

    @admin.display(ordering="references_count", description=_("Number of References"))
    def references_count(self, writer):
        return model_changelist_url_to_html(
            app="references",
            model="reference",
            query_key="writers",
            query_val=writer.id,
            placeholder=writer.references.count(),
        )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            "references",
        )
