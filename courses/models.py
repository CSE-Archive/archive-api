from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, TagField
from courses.managers import CourseManager


class Course(BaseModel):

    class Types(models.IntegerChoices):
        SPECIALIZED = 1, _("Specialized")
        OPTIONAL = 2, _("Optional")
        BASIC = 3, _("Basic")
        GENERAL = 4, _("General")
    
    UNITS_CHOICES = list((u, _(str(u))) for u in range(1, settings.MAX_COURSE_UNIT+1))

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=127,
    )
    en_title = models.CharField(
        verbose_name=_("Title in English"),
        max_length=127,
        null=True,
        blank=True,
    )
    units = models.PositiveSmallIntegerField(
        verbose_name=_("Units"),
        choices=UNITS_CHOICES,
    )
    type = models.PositiveSmallIntegerField(
        verbose_name=_("Type"),
        choices=Types.choices,
    )
    tag = TagField()
    known_as = models.CharField(
        verbose_name=_("Known As"),
        max_length=127,
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        null=True,
        blank=True,
    )
    
    objects = CourseManager()

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        ordering = ("type", "title",)


class CourseRelation(models.Model):

    class Types(models.IntegerChoices):
        CO = 1, _("Corequisite")
        PRE = 2, _("Prerequisite")
        INC = 3, _("Incompatible")

    type = models.PositiveSmallIntegerField(
        verbose_name=_("Type"),
        choices=Types.choices,
    )
    course_from = models.ForeignKey(
        Course,
        verbose_name=_("Course From"),
        on_delete=models.CASCADE,
        related_name="relations_from",
    )
    course_to = models.ForeignKey(
        Course,
        verbose_name=_("Course To"),
        on_delete=models.CASCADE,
        related_name="relations_to",
    )

    def __str__(self) -> str:
        return f"{self.course_from.title} -> {self.course_to.title} : ({self.type})"

    class Meta:
        verbose_name = _("Course Relation")
        verbose_name_plural = _("Course Relations")
        constraints = [
            models.UniqueConstraint(
                fields=['course_from', 'course_to'],
                name="unique_relation_reverse",
                violation_error_message=_("Two courses can have at most one relationship."),
             ),
            models.CheckConstraint(
                name="prevent_self_relation",
                check=~models.Q(course_from=models.F("course_to")),
                violation_error_message=_("Courses cannot have a relationship to themselves."),
            )
        ]
