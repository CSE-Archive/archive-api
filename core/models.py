from typing import Any

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields as contenttypes_fields

from core.helpers import uuid_generator


class User(AbstractUser):
    email = models.EmailField(unique=True)


class Link(models.Model):
    url = models.URLField(
        verbose_name=_("Url"),
        max_length=255,
    )
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=63,
    )

    linked_type = models.ForeignKey(
        ContentType,
        verbose_name=_("Liked Type"),
        on_delete=models.CASCADE,
        related_name='links',
    )
    linked_id = models.PositiveIntegerField(
        verbose_name=_("Liked ID")
    )
    linked = contenttypes_fields.GenericForeignKey('linked_type', 'linked_id')

    def __str__(self) -> str:
        return self.url

    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("Links")


class ShortUuidField(models.CharField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs['unique'] = True
        kwargs['default'] = uuid_generator
        kwargs['max_length'] = settings.UUID_LENGTH
        kwargs['editable'] = False
        kwargs['db_index'] = True
        kwargs['verbose_name'] = _("UUID")
        super().__init__(*args, **kwargs)


class BaseModel(models.Model):
    uuid = ShortUuidField()
    is_published = models.BooleanField(
        verbose_name=_("Is Published"),
        default=False,
    )
    created_time = models.DateTimeField(
        verbose_name=_("Created Time"),
        auto_now_add=True,
    )
    modified_time = models.DateTimeField(
        verbose_name=_("Modified Time"),
        auto_now=True,
    )

    class Meta:
        abstract = True


class BaseManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(is_published=True)
    
    def get_raw_queryset(self) -> QuerySet:
        return super().get_queryset()
    
    def get_by_natural_key(self, uuid: str):
        return self.get(uuid=uuid)
