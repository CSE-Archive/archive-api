from django.conf import settings
from django.contrib import admin
from django.utils import translation
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
import nested_admin

from core.models import User, Link


@admin.register(User)
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


class LinkInlineAdmin(GenericTabularInline):
    model = Link
    extra = 0
    ct_field = 'linked_type'
    ct_fk_field = 'linked_id'


class LinkNestedInlineAdmin(nested_admin.NestedGenericTabularInline):
    model = Link
    extra = 0
    ct_field = 'linked_type'
    ct_fk_field = 'linked_id'


class BaseAdminMixin:
    def get_queryset(self, request):
        qs = self.model._default_manager.get_raw_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
