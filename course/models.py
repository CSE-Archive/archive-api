import datetime
from django.db import models


class Course(models.Model):
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

    unit = models.PositiveSmallIntegerField()
    term_in_chart = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=255)
    en_title = models.CharField(max_length=255)
    tag = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)


class Session(models.Model):
    def _year_choices():
        return [(r, r) for r in range(2000, datetime.date.today().year+1)]

    FALL = "FA"
    SPRING = "SP"
    SUMMER = "SU"

    SEMESTER_CHOICES = [
        (FALL, "Fall"),
        (SPRING, "Spring"),
        (SUMMER, "Summer"),
    ]

    semester = models.CharField(max_length=2, choices=SEMESTER_CHOICES)
    year = models.PositiveSmallIntegerField(choices=_year_choices)


class TA(models.Model):
    full_name = models.CharField(max_length=255)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)


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
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True, editable=True)
	type = models.CharField(max_length=1, choices=TYPE_CHOICES)
	session = models.ForeignKey(Session, on_delete=models.PROTECT)


class Requisite(models.Model):
	CO = "C"
	PRE = "P"

	TYPE_CHOICES = [
		(CO, "Corequisite"),
		(PRE, "Prerequisite"),
	]

	type = models.CharField(max_length=1, choices=TYPE_CHOICES)
	course1 = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course1")
	course2 = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course2")
