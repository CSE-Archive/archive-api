from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes import fields as contenttypes_fields

from core.models import BaseModel, Link
from core.validators import MaxImageSizeValidator
from courses.models import Course
from references.managers import ReferenceManager, AuthorManager


class Author(models.Model):
    full_name = models.CharField(
        verbose_name=_("Full Name"),
        max_length=255,
        unique=True,
    )

    objects = AuthorManager()

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")


class Reference(BaseModel):

    class Types(models.IntegerChoices):
        BOOK = 1, _("Book")
        SOLUTION = 2, _("Solution")
        SLIDE = 3, _("Slide")
        HANDOUT = 4, _("Handout")

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255,
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
        related_query_name='linked_references',
    )
    cover_image = models.ImageField(
        verbose_name=_("Cover Image"),
        upload_to="images/references/",
        null=True,
        validators=[MaxImageSizeValidator(1)],
    )
    authors = models.ManyToManyField(
        Author,
        verbose_name=_("Authors"),
        related_name="references",
        blank=True,
    )
    collector = models.CharField(
        verbose_name=_("Collector"),
        max_length=255,
        null=True,
    )
    courses = models.ManyToManyField(
        Course,
        verbose_name=_("Courses"),
        related_name="references",
        blank=True,
    )
    related_references = models.ManyToManyField(
        'self',
        verbose_name=_("Related References"),
        blank=True,
    )

    objects = ReferenceManager()

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Reference")
        verbose_name_plural = _("References")
        ordering = ("modified_time", "created_time",)