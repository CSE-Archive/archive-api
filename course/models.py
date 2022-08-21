import jdatetime

from teacher.models import Teacher
from reference.models import Reference
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext as _


class Course(models.Model):
    BASIC = "B"
    GENERAL = "G"
    OPTIONAL = "O"
    SPECIALIZED = "S"

    TYPE_CHOICES = [
        (BASIC, "پایه"),
        (GENERAL, "عمومی"),
        (OPTIONAL, "اختیاری"),
        (SPECIALIZED, "تخصصی"),
    ]

    UNIT_CHOICES = [(u, u) for u in range(1, 3+1)]

    title = models.CharField(
        verbose_name=_("عنوان"),
        max_length=255,
    )
    en_title = models.CharField(
        verbose_name=_("عنوان به انگلیسی"),
        max_length=255,
    )
    unit = models.PositiveSmallIntegerField(
        verbose_name=_("واحد"),
        choices=UNIT_CHOICES,
    )
    type = models.CharField(
        verbose_name=_("نوع"),
        max_length=1,
        choices=TYPE_CHOICES,
    )
    tag = models.CharField(
        verbose_name=_("تگ"),
        max_length=255,
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("توضیحات"),
        null=True,
        blank=True,
    )
    references = models.ManyToManyField(
        Reference,
        related_name="courses",
        verbose_name=_("مراجع"),
        blank=True,
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "درس"
        verbose_name_plural = "دروس"


class ClassroomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset() \
            .select_related("course") \
            .order_by("-year", "semester", "course__en_title")


class TA(models.Model):
    full_name = models.CharField(
        verbose_name=_("نام و نام خانوادگی"),
        max_length=255,
    )

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name = "گریدر"
        verbose_name_plural = "گریدرها"


class Classroom(models.Model):
    def _current_year():
        return jdatetime.date.today().year

    MIN_YEAR = 1300

    FIRST = "1"
    SECOND = "2"
    SUMMER = "S"

    SEMESTER_CHOICES = [
        (FIRST, "اول"),
        (SECOND, "دوم"),
        (SUMMER, "تابستان"),
    ]

    objects = ClassroomManager()

    year = models.PositiveSmallIntegerField(
        verbose_name=_("سال"),
        validators=[
            MinValueValidator(MIN_YEAR),
            MaxValueValidator(_current_year)
        ],
    )
    semester = models.CharField(
        verbose_name=_("نیم سال"),
        max_length=1,
        choices=SEMESTER_CHOICES,
    )
    course = models.ForeignKey(
        Course,
        verbose_name=_("درس"),
        on_delete=models.PROTECT,
        related_name="classrooms",
    )
    teachers = models.ManyToManyField(
        Teacher,
        related_name="classrooms",
        verbose_name=_("اساتید"),
    )
    tas = models.ManyToManyField(
        TA,
        related_name="classrooms",
        verbose_name=_("گریدرها"),
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.year} - {self.semester} - {self.course.en_title}"

    class Meta:
        verbose_name = "کلاس"
        verbose_name_plural = "کلاس‌ها"
        unique_together = ("year", "semester", "course",)


class Resource(models.Model):
    MIDTERM = "M"
    FINAL = "F"
    PROJECT = "P"
    HOMEWORK = "H"
    QUIZ = "Q"
    OTHER = "O"

    TYPE_CHOICES = [
        (MIDTERM, "میانترم"),
        (FINAL, "پایانترم"),
        (PROJECT, "پروژه"),
        (HOMEWORK, "تمرین"),
        (QUIZ, "کوییز"),
        (OTHER, "دیگر"),
    ]

    file = models.FileField(
        verbose_name=_("فایل"),
        upload_to="files/resources/",
    )
    title = models.CharField(
        verbose_name=_("عنوان"),
        max_length=255,
    )
    type = models.CharField(
        verbose_name=_("نوع"),
        max_length=1,
        choices=TYPE_CHOICES,
    )
    date_created = models.DateTimeField(
        verbose_name=_("تاریخ اضافه شدن"),
        auto_now_add=True,
    )
    date_modified = models.DateTimeField(
        verbose_name=_("آخرین ویرایش"),
        auto_now=True,
    )
    classroom = models.ForeignKey(
        Classroom,
        verbose_name=_("کلاس"),
        on_delete=models.PROTECT,
        related_name="resources",
    )
    support_url = models.URLField(
        verbose_name=_("لینک دانلود حمایتی"),
        max_length=255,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.classroom} - {self.title}"

    class Meta:
        verbose_name = "منبع"
        verbose_name_plural = "منابع"


class Requisite(models.Model):
    CO = "C"
    PRE = "P"

    TYPE_CHOICES = [
        (CO, "هم‌نیاز"),
        (PRE, "پیش‌نیاز"),
    ]

    type = models.CharField(
        verbose_name=_("نوع"),
        max_length=1,
        choices=TYPE_CHOICES,
    )
    course_from = models.ForeignKey(
        Course,
        verbose_name=_("درس مبدا"),
        on_delete=models.CASCADE,
        related_name="requisites_from",
    )
    course_to = models.ForeignKey(
        Course,
        verbose_name=_("درس مقصد"),
        on_delete=models.CASCADE,
        related_name="requisites_to",
    )

    def __str__(self) -> str:
        return f"{self.course_from.en_title} -> {self.course_to.en_title} : ({self.type})"

    class Meta:
        verbose_name = "نیاز"
        verbose_name_plural = "نیازها"
        unique_together = ("course_from", "course_to",)
