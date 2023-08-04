from django.contrib import admin
from django.utils.translation import gettext_lazy as _
import nested_admin

from core.helpers import gregorian_to_jalali, model_change_url_to_html
from core.admin import BaseAdminMixin, LinkInlineAdmin, LinkNestedInlineAdmin
from resources.models import Resource


class ResourceNestedInlineAdmin(nested_admin.NestedTabularInline):
    model = Resource
    extra = 0
    verbose_name = _("Resource")
    verbose_name_plural = _("Resources")
    inlines = (LinkNestedInlineAdmin,)


@admin.register(Resource)
class ResourceAdmin(BaseAdminMixin, admin.ModelAdmin):
    inlines = (LinkInlineAdmin,)
    autocomplete_fields = ("classroom",)
    list_per_page = 25
    list_display = ("uuid", "title", "type", "modified_time_",
                    "created_time_", "classroom_",)
    list_select_related = ("classroom", "classroom__course",)
    list_filter = ("modified_time", "created_time", "type",)
    extra_allowed_lookups = ("classroom__id", "classroom__course__id",)
    search_fields = ("uuid", "title", "classroom__course__title",
                     "classroom__course__en_title",)

    @admin.display(ordering="classroom_", description=_("Classroom"))
    def classroom_(self, instance: Resource):
        return model_change_url_to_html(
            app="classrooms",
            model="classroom",
            args=(instance.classroom.id,),
            placeholder=str(instance.classroom),
        )

    @admin.display(ordering="created_time", description=_("Created Time"))
    def created_time_(self, instance: Resource):
        return gregorian_to_jalali(instance.created_time)

    @admin.display(ordering="modified_time", description=_("Modified Time"))
    def modified_time_(self, instance: Resource):
        return gregorian_to_jalali(instance.modified_time)
    
    def lookup_allowed(self, lookup, *args, **kwargs):
        return (
            lookup in self.extra_allowed_lookups
            or super().lookup_allowed(lookup, *args, **kwargs)
        )

