import datetime
from django.db import models


class Course(models.Model):
    def _unit_choices():
        return [(u, u) for u in range(1, 3+1)]

    def _term_in_chart_choices():
        return [(t, t) for t in range(1, 8+1)]

    BASIC = "B"
    GENERAL = "G"
    OPTIONAL = "O"
    SPECIALIZED = "S"

    TYPE_CHOICES = [
        (BASIC, "Basic"),
        (GENERAL, "General"),
        (OPTIONAL, "Optional"),
        (SPECIALIZED, "Specialized"),
    ]

    unit = models.PositiveSmallIntegerField(choices=_unit_choices())
    term_in_chart = models.PositiveSmallIntegerField(
        choices=_term_in_chart_choices(),
    )
    title = models.CharField(max_length=255)
    en_title = models.CharField(max_length=255)
    tag = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)

    def __str__(self) -> str:
        return self.title


class Session(models.Model):
    def _year_choices():
        return [(y, y) for y in range(2000, datetime.date.today().year+1)]

    FALL = "FA"
    SPRING = "SP"
    SUMMER = "SU"

    SEMESTER_CHOICES = [
        (FALL, "Fall"),
        (SPRING, "Spring"),
        (SUMMER, "Summer"),
    ]

    year = models.PositiveSmallIntegerField(choices=_year_choices())
    semester = models.CharField(max_length=2, choices=SEMESTER_CHOICES)
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="sessions",
    )

    def __str__(self) -> str:
        return f"{self.year} - {self.semester} - {self.course.en_title}"


class TA(models.Model):
    full_name = models.CharField(max_length=255)
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name="tas",
    )

    def __str__(self) -> str:
        return self.full_name


class Resource(models.Model):
    MIDTERM = "M"
    FINAL = "F"
    HOMEWORK = "H"
    QUIZ = "Q"
    OTHER = "O"

    TYPE_CHOICES = [
        (MIDTERM, "Midterm"),
        (FINAL, "Final"),
        (HOMEWORK, "Homework"),
        (QUIZ, "Quiz"),
        (OTHER, "Other"),
    ]

    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    session = models.ForeignKey(
        Session,
        on_delete=models.PROTECT,
        related_name="resources",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.session} - {self.title}"


class Requisite(models.Model):
    CO = "C"
    PRE = "P"

    TYPE_CHOICES = [
        (CO, "Corequisite"),
        (PRE, "Prerequisite"),
    ]

    course_from = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="requisites_from",
    )
    course_to = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="requisites_to",
    )
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)

    def __str__(self) -> str:
        return f"{self.course_from.en_title} -> {self.course_to.en_title} : ({self.type})"
