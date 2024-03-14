from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.utils import model_ngettext
from django.utils.translation import gettext_lazy, gettext as _
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
                'classes': ('wide',),
                'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name'),
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
    @admin.action(description=gettext_lazy('Publish selected %(verbose_name_plural)s'))
    def make_published(self, modeladmin, request, queryset):
        published_count = queryset.update(is_published=False)
        self.message_user(
            request,
            _('Successfully published %(count)d %(items)s.') % {
                'count': published_count,
                'items': modeladmin.model._meta.verbose_name.title() if request.LANGUAGE_CODE == 'fa'
                         else model_ngettext(modeladmin.model._meta, published_count),
            },
            messages.SUCCESS,
        )

    @admin.action(description=gettext_lazy('Unpublish selected %(verbose_name_plural)s'))
    def make_unpublished(self, modeladmin, request, queryset):
        unpublished_count = queryset.update(is_published=False)
        self.message_user(
            request,
            _('Successfully unpublished %(count)d %(items)s.') % {
                'count': unpublished_count,
                'items': modeladmin.model._meta.verbose_name.title() if request.LANGUAGE_CODE == 'fa'
                         else model_ngettext(modeladmin.model._meta, unpublished_count),
            },
            messages.SUCCESS,
        )

    def _get_base_actions(self):
        self.admin_site._actions.update({
            'make_published': self.make_published,
            'make_unpublished': self.make_unpublished,
        })
        return super()._get_base_actions()

    def get_queryset(self, request):
        qs = self.model._default_manager.get_raw_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs
