from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes import fields as contenttypes_fields

from core.models import BaseModel, Link
from classrooms.models import Classroom
from resources.managers import ResourceManager


class Resource(BaseModel):

    class Types(models.IntegerChoices):
        MIDTERM = 1, _("Midterm")
        FINAL = 2, _("Final")
        PROJECT = 3, _("Project")
        HOMEWORK = 4, _("Homework")
        QUIZ = 5, _("Quiz")
        OTHER = 6, _("Other")

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255,
        null=True,
    )
    type = models.PositiveSmallIntegerField(
        verbose_name=_("Type"),
        choices=Types.choices,
    )
    notes = models.CharField(
        verbose_name=_("Notes"),
        max_length=255,
        null=True,
    )
    links = contenttypes_fields.GenericRelation(
        Link,
        verbose_name=_("Links"),
        content_type_field='linked_type',
        object_id_field='linked_id',
        related_query_name='linked_resources',
    )
    classroom = models.ForeignKey(
        Classroom,
        verbose_name=_("Classroom"),
        on_delete=models.PROTECT,
        related_name="resources",
    )

    objects = ResourceManager()

    def __str__(self) -> str:
        return f"{self.classroom} - {self.title}"

    class Meta:
        verbose_name = _("Resource")
        verbose_name_plural = _("Resources")
        ordering = ("modified_time", "created_time",)