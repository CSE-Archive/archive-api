from .models import Author, Reference
from core.helpers import image_url_to_html, gregorian_to_jalali, model_changelist_url_to_html
from course.models import Course
from django.contrib import admin
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
        return image_url_to_html(
            image=reference.cover_image,
            style="contain",
            width=500,
            open_in_new_tab=True,
        )

    @admin.display(description=_("تصویر جلد"))
    def cover_image_(self, reference):
        return image_url_to_html(
            image=reference.cover_image,
            style="cover",
            width=100,
            height=100,
            open_in_new_tab=True,
        )

    @admin.display(ordering="authors_count", description=_("تعداد نویسنده‌ها"))
    def authors_count(self, reference):
        return reference.authors.count()
    
    @admin.display(ordering="courses_count", description=_("تعداد درس‌ها"))
    def courses_count(self, reference):
        return model_changelist_url_to_html(
            app="course",
            model="course",
            query_key="references",
            query_val=reference.id,
            placeholder=reference.courses.count(),
        )

    @admin.display(ordering="date_created", description=_("تاریخ اضافه شدن"))
    def date_created_(self, reference):
        return gregorian_to_jalali(reference.date_created)

    @admin.display(ordering="date_modified", description=_("آخرین ویرایش"))
    def date_modified_(self, reference):
        return gregorian_to_jalali(reference.date_modified)

    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related("authors",)
