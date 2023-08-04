from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes import fields as contenttypes_fields

from core.models import BaseModel, Link, ShortUuidField
from core.validators import MaxImageSizeValidator
from professors.managers import DepartmentManager, ProfessorManager


class Department(models.Model):
    uuid = ShortUuidField()
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=63,
        blank=True,
    )
    name_en = models.CharField(
        verbose_name=_("Name in English"),
        max_length=63,
        blank=True,
    )

    objects = DepartmentManager()

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")
        ordering = ("name",)


class Professor(BaseModel):
    first_name = models.CharField(
        verbose_name=_("First Name"),
        max_length=63,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name=_("Last Name"),
        max_length=63,
        blank=True,
    )
    honorific = models.CharField(
        verbose_name=_("Honorific"),
        max_length=31,
        blank=True,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        verbose_name=_("Department"),
        null=True,
    )
    about = models.TextField(
        verbose_name=_("About"),
        blank=True,
        default="",
    )
    tag = models.CharField(
        verbose_name=_("Tag"),
        max_length=127,
        blank=True,
    )
    image = models.ImageField(
        verbose_name=_("Image"),
        upload_to="images/professors/",
        null=True,
        blank=True,
        validators=[MaxImageSizeValidator(1)],
    )
    has_detail = models.BooleanField(
        verbose_name=_("Has Detail"),
        default=True,
    )
    links = contenttypes_fields.GenericRelation(
        Link,
        verbose_name=_("Links"),
        content_type_field='linked_type',
        object_id_field='linked_id',
        related_query_name='linked_resources',
    )

    objects = ProfessorManager()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("Professor")
        verbose_name_plural = _("Professors")
        ordering = ("last_name", "first_name",)


class Email(models.Model):
    address = models.EmailField(
        verbose_name=_("Address"),
        unique=True,
    )
    professor = models.ForeignKey(
        Professor,
        verbose_name=_("Professor"),
        on_delete=models.CASCADE,
        related_name="emails",
    )

    def __str__(self) -> str:
        return self.address

    class Meta:
        verbose_name = _("Email")
        verbose_name_plural = _("Emails")
