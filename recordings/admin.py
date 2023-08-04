from django.contrib import admin
from django.utils.translation import gettext_lazy as _
import nested_admin

from core.helpers import gregorian_to_jalali, model_change_url_to_html
from core.admin import BaseAdminMixin, LinkNestedInlineAdmin
from recordings.models import RecordedClassroom, RecordedSession


class RecordedSessionNestedInlineAdmin(nested_admin.NestedTabularInline):
    model = RecordedSession
    extra = 0
    verbose_name = _("Recored Session")
    verbose_name_plural = _("Recored Sessions")
    inlines = (LinkNestedInlineAdmin,)


class RecordedClassroomNestedInlineAdmin(nested_admin.NestedTabularInline):
    model = RecordedClassroom
    extra = 0
    verbose_name = _("Recored Classroom")
    verbose_name_plural = _("Recored Classrooms")
    inlines = (RecordedSessionNestedInlineAdmin,)


@admin.register(RecordedClassroom)
class RecordedClassAdmin(BaseAdminMixin, nested_admin.NestedModelAdmin):
    inlines = (LinkNestedInlineAdmin, RecordedSessionNestedInlineAdmin,)
    autocomplete_fields = ("classroom",)
    list_per_page = 25
    list_display = ("uuid", "modified_time_", "created_time_",
                    "classroom_", "sessions_count",)
    list_select_related = ("classroom__course",)
    list_filter = ("modified_time", "created_time",)
    extra_allowed_lookups = ("classroom__id", "classroom__course__id",)
    search_fields = ("uuid", "classroom__course__title",
                     "classroom__course__en_title",)

    @admin.display(ordering="classroom_", description=_("Classroom"))
    def classroom_(self, instance: RecordedClassroom):
        return model_change_url_to_html(
            app="classrooms",
            model="classroom",
            args=(instance.classroom.id,),
            placeholder=str(instance.classroom),
        )

    @admin.display(ordering="sessions_count", description=_("Number of sessions"))
    def sessions_count(self, instance: RecordedClassroom):
        return instance.sessions.count()

    @admin.display(ordering="created_time", description=_("Created Time"))
    def created_time_(self, instance: RecordedClassroom):
        return gregorian_to_jalali(instance.created_time)

    @admin.display(ordering="modified_time", description=_("Modified Time"))
    def modified_time_(self, instance: RecordedClassroom):
        return gregorian_to_jalali(instance.modified_time)
    
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related(
                "sessions",
            )

    def lookup_allowed(self, lookup, *args, **kwargs):
        return (
            lookup in self.extra_allowed_lookups
            or super().lookup_allowed(lookup, *args, **kwargs)
        )
