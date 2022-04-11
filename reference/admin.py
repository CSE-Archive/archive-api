from . import models
from django.contrib import admin
from django.urls import reverse
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.utils.translation import gettext as _
from django_jalali.admin.filters import JDateFieldListFilter

import django_jalali.admin as jadmin  # for adding jalali calender widget


class AuthorInline(admin.TabularInline):
    model = models.Author
    extra = 0


@admin.register(models.Reference)
class ReferenceAdmin(admin.ModelAdmin):
    inlines = (AuthorInline,)
    list_per_page = 10
    list_display = ("id", "title", "date_modified",
                    "date_created", "cover_image", "authors_count",)
    list_filter = (("date_modified", JDateFieldListFilter),
                   ("date_created", JDateFieldListFilter),)
    search_fields = ("title",)

    @admin.display(ordering="authors_count", description=_("تعداد نویسنده‌ها"))
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
    list_display = ("id", "reference_", "content_object_",)
    list_filter = ("reference",)

    @admin.display(ordering="reference_", description=_("مرجع"))
    def reference_(self, reference_item):
        url = (
            reverse("admin:reference_reference_changelist")
            + str(reference_item.reference.id)
            + "/"
            + "change"
        )
        return format_html('<a href="{}">{}</a>', url, reference_item.reference.title)

    @admin.display(ordering="content_object_", description=_("محتوای مربوطه"))
    def content_object_(self, reference_item):
        return reference_item.content_object
