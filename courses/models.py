from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from courses.managers import CourseManager


class Course(BaseModel):

    class Types(models.IntegerChoices):
        SPECIALIZED = 1, _("Specialized")
        OPTIONAL = 2, _("Optional")
        BASIC = 3, _("Basic")
        GENERAL = 4, _("General")
    
    UNITS_CHOICES = ((u, _(str(u))) for u in range(1, settings.MAX_COURSE_UNIT+1))

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=127,
    )
    en_title = models.CharField(
        verbose_name=_("Title in English"),
        max_length=127,
        null=True,
    )
    units = models.PositiveSmallIntegerField(
        verbose_name=_("Units"),
        choices=UNITS_CHOICES,
    )
    type = models.PositiveSmallIntegerField(
        verbose_name=_("Type"),
        choices=Types.choices,
    )
    tag = models.CharField(
        verbose_name=_("Tag"),
        max_length=127,
        null=True,
    )
    known_as = models.CharField(
        verbose_name=_("Known As"),
        max_length=127,
        null=True,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        null=True,
        default="",
    )
    
    objects = CourseManager()

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        ordering = ("type", "title",)


class Requisite(models.Model):

    class Types(models.IntegerChoices):
        CO = 1, _("Corequisite")
        PRE = 2, _("Prerequisite")

    type = models.PositiveSmallIntegerField(
        verbose_name=_("Type"),
        choices=Types.choices,
    )
    course_from = models.ForeignKey(
        Course,
        verbose_name=_("Course From"),
        on_delete=models.CASCADE,
        related_name="requisites_from",
    )
    course_to = models.ForeignKey(
        Course,
        verbose_name=_("Course To"),
        on_delete=models.CASCADE,
        related_name="requisites_to",
    )

    def __str__(self) -> str:
        return f"{self.course_from.en_title} -> {self.course_to.en_title} : ({self.type})"

    class Meta:
        verbose_name = _("Requisite")
        verbose_name_plural = _("Requisities")
        unique_together = ("course_from", "course_to",)
