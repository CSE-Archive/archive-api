from django.db import models
from django.utils.translation import gettext_lazy as _

from courses.models import Course


class ChartNode(models.Model):

    class Semesters(models.IntegerChoices):
        ONE = 1, "1"
        TWO = 2, "2"
        THREE = 3, "3"
        FOUR = 4, "4"
        FIVE = 5, "5"
        SIX = 6, "6"
        SEVEN = 7, "7"
        EIGHT = 8, "8"

    semester = models.PositiveSmallIntegerField(
        verbose_name=_("Semester"),
        choices=Semesters.choices,
    )
    column = models.PositiveSmallIntegerField(
        verbose_name=_("Column"),
    )
    course = models.OneToOneField(
        Course,
        verbose_name=_("Course"),
        on_delete=models.CASCADE,
        related_name="chart_node",
        null=True,
        blank=True,
    )
    type = models.PositiveSmallIntegerField(
        verbose_name=_("Type"),
        choices=Course.Types.choices,
        null=True,
        blank=True,
    )
    units = models.PositiveSmallIntegerField(
        verbose_name=_("Units"),
        choices=Course.UNITS_CHOICES,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("Chart Node")
        verbose_name_plural = _("Chart Nodes")
        ordering = ("semester", "column",)
        constraints = [
            models.CheckConstraint(
                check=models.Q(course__isnull=True, type__isnull=False, units__isnull=False)
                    | models.Q(course__isnull=False, type__isnull=True, units__isnull=True),
                name="linked_to_course_or_not",
                violation_error_message=_("Nodes must either be related to a course or have a value in their type and unit fields."),
            )
        ]
