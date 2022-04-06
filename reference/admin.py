from . import models
from django.contrib import admin
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.urls import reverse
from django.db.models import Count, OuterRef, Subquery
from django.utils.html import format_html, urlencode


class AuthorInline(admin.TabularInline):
    model = models.Author
    extra = 0


@admin.register(models.Reference)
class ReferenceAdmin(admin.ModelAdmin):
    inlines = (AuthorInline,)
    list_per_page = 10
    list_display = ("id", "title", "date_modified",
                    "date_created", "cover_image", "authors_count",)
    list_filter = ("date_modified", "date_created",)
    search_fields = ("title",)

    @admin.display(ordering="authors_count")
    def authors_count(self, reference):
        url = (
            reverse("admin:reference_author_changelist")
            + "?"
            + urlencode({
                "reference__id": str(reference.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, reference.authors_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            authors_count=Count("author"),
        )


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    autocomplete_fields = ("reference",)
    list_per_page = 10
    list_display = ("id", "full_name", "reference")
    list_filter = ("reference",)
    search_fields = ("full_name",)


@admin.register(models.ReferenceItem)
class ReferenceItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ("reference",)
    list_per_page = 10
    list_display = ("id", "reference_", "content_object",)
    list_filter = ("reference",)

    @admin.display(ordering="reference_")
    def reference_(self, referenceitem):
        url = (
            reverse("admin:reference_reference_changelist")
            + str(referenceitem.reference.id)
            + "/"
            + "change"
        )
        return format_html('<a href="{}">{}</a>', url, referenceitem.reference.title)
