from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes import fields as contenttypes_fields

from core.models import BaseModel, Link
from core.helpers import uuid_generator
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
        blank=True,
    )
    type = models.PositiveSmallIntegerField(
        verbose_name=_("Type"),
        choices=Types.choices,
    )
    is_solution = models.BooleanField(
        verbose_name=_("Is Solution?"),
        default=False,
    )
    notes = models.CharField(
        verbose_name=_("Notes"),
        max_length=255,
        null=True,
        blank=True,
    )
    file = models.FileField(
        _("File"),
        null=True,
        blank=True,
        max_length=255,
        upload_to='resources',
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
        return f"{self.classroom} - {self.title or self.get_type_display()}"

    def generate_unique_name(self) -> str:
        return "{course_title}-{type}-{class_year}{class_semester}-{random_uuid}".format(
            course_title=self.classroom.course.en_title.replace(' ', ''),
            type=self.get_type_display(),
            class_year=self.classroom.year,
            class_semester=self.classroom.semester,
            random_uuid=uuid_generator(),
        )

    class Meta:
        verbose_name = _("Resource")
        verbose_name_plural = _("Resources")
        ordering = ("-modified_time", "-created_time",)
