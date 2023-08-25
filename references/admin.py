from django.contrib import admin
from django.utils.translation import gettext_lazy as _
import nested_admin

from core.admin import BaseAdminMixin, LinkNestedInlineAdmin
from core.helpers import image_url_to_html, gregorian_to_jalali, model_changelist_url_to_html
from references.models import Author, Reference


class ReferenceNestedInlineAdmin(nested_admin.NestedTabularInline):
    model = Reference.authors.through
    extra = 0
    autocomplete_fields = ("reference",)
    verbose_name = _("Reference")
    verbose_name_plural = _("References")


class CourseInlineAdmin(nested_admin.NestedTabularInline):
    model = Reference.courses.through
    extra = 0
    autocomplete_fields = ("course",)
    verbose_name = _("Course")
    verbose_name_plural = _("Courses")


@admin.register(Reference)
class ReferenceAdmin(BaseAdminMixin, nested_admin.NestedModelAdmin):
    inlines = (CourseInlineAdmin, LinkNestedInlineAdmin,)
    list_per_page = 25
    list_display = ("uuid", "cover_image_", "title", "type", "collector", "authors_count",
                    "courses_count", "modified_time_", "created_time_",)
    readonly_fields = ("preview",)
    list_filter = ("modified_time", "created_time", "type", "courses__id",)
    search_fields = ("uuid", "title", "collector", "authors__full_name",)

    @admin.display(description=_("Cover Image Preview"))
    def preview(self, instance: Reference):
        return image_url_to_html(
            image=instance.cover_image,
            style="contain",
            width=500,
            open_in_new_tab=True,
        )

    @admin.display(description=_("Cover Image"))
    def cover_image_(self, instance: Reference):
        return image_url_to_html(
            image=instance.cover_image,
            style="cover",
            width=100,
            height=100,
            open_in_new_tab=True,
        )

    @admin.display(ordering="authors_count", description=_("Number of Authors"))
    def authors_count(self, instance: Reference):
        return model_changelist_url_to_html(
            app="references",
            model="author",
            query_key="references",
            query_val=instance.id,
            placeholder=instance.authors.count(),
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
            "authors",
            "courses",
        )


@admin.register(Author)
class AuthorAdmin(nested_admin.NestedModelAdmin):
    inlines = (ReferenceNestedInlineAdmin,)
    list_per_page = 25
    list_display = ("id", "full_name", "references_count",)
    search_fields = ("full_name",)

    @admin.display(ordering="references_count", description=_("Number of References"))
    def references_count(self, author):
        return model_changelist_url_to_html(
            app="references",
            model="reference",
            query_key="authors",
            query_val=author.id,
            placeholder=author.references.count(),
        )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            "references",
        )
