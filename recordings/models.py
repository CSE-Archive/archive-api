from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes import fields as contenttypes_fields

from core.models import BaseModel, Link
from classrooms.models import Classroom
from recordings.managers import RecordedClassroomManager


class RecordedClassroom(BaseModel):
    notes = models.CharField(
        verbose_name=_("Notes"),
        max_length=255,
        null=True,
    )
    classroom = models.OneToOneField(
        Classroom,
        verbose_name=_("Classroom"),
        on_delete=models.PROTECT,
        related_name="recordings",
    )
    links = contenttypes_fields.GenericRelation(
        Link,
        verbose_name=_("Links"),
        content_type_field='linked_type',
        object_id_field='linked_id',
        related_query_name='linked_recorded_classrooms',
    )

    objects = RecordedClassroomManager()

    def __str__(self) -> str:
        return f"{self.classroom}"

    class Meta:
        verbose_name = _("Recored Classroom")
        verbose_name_plural = _("Recored Classrooms")
        ordering = ("modified_time", "created_time",)


class RecordedSession(models.Model):
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255,
    )
    order = models.FloatField(
        verbose_name=_("Order")
    )
    links = contenttypes_fields.GenericRelation(
        Link,
        verbose_name=_("Links"),
        content_type_field='linked_type',
        object_id_field='linked_id',
        related_query_name='linked_recorded_sessions',
    )
    recorded_classroom = models.ForeignKey(
        RecordedClassroom,
        verbose_name=_("Recored Classroom"),
        on_delete=models.PROTECT,
        related_name="sessions",
    )

    def __str__(self) -> str:
        return f"{self.recorded_classroom} {self.title}"

    class Meta:
        verbose_name = _("Recored Session")
        verbose_name_plural = _("Recored Sessions")
        ordering = ("order", "id")
