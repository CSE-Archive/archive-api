from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from core.models import BaseModel, ShortUuidField
from core.validators import MaxCurrentYearValidator
from courses.models import Course
from professors.models import Professor
from classrooms.managers import ClassroomManager, TaManager


class TA(models.Model):
    uuid = ShortUuidField()
    full_name = models.CharField(
        verbose_name=_("Full Name"),
        max_length=255,
        unique=True
    )

    objects = TaManager()

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name = _("TA")
        verbose_name_plural = _("TAs")
        ordering = ("full_name",)


class Classroom(BaseModel):

    class Semesters(models.IntegerChoices):
        FIRST = 1, _("First")
        SECOND = 2, _("Second")
        SUMMER = 3, _("Summer")
    
    year = models.PositiveSmallIntegerField(
        verbose_name=_("Year"),
        validators=[
            MinValueValidator(settings.MIN_YEAR),
            MaxCurrentYearValidator()
        ],
    )
    semester = models.PositiveSmallIntegerField(
        verbose_name=_("Semester"),
        choices=Semesters.choices,
    )
    course = models.ForeignKey(
        Course,
        verbose_name=_("Course"),
        on_delete=models.PROTECT,
        related_name="classrooms",
    )
    professors = models.ManyToManyField(
        Professor,
        verbose_name=_("Professors"),
        related_name="classrooms",
        blank=True,
    )
    tas = models.ManyToManyField(
        TA,
        verbose_name=_("TAs"),
        related_name="classrooms",
        blank=True,
    )

    objects = ClassroomManager()

    def __str__(self) -> str:
        return f"{self.year} - {self.semester} - {self.course.title}"

    class Meta:
        verbose_name = _("Classroom")
        verbose_name_plural = _("Classrooms")
        ordering = ("-year", "-semester", "course__type", "course__title",)
