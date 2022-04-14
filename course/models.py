import jdatetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext as _


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
        (BASIC, "پایه"),
        (GENERAL, "عمومی"),
        (OPTIONAL, "اختیاری"),
        (SPECIALIZED, "تخصصی"),
    ]

    unit = models.PositiveSmallIntegerField(
        verbose_name=_("واحد"),
        choices=_unit_choices(),
    )
    term_in_chart = models.PositiveSmallIntegerField(
        verbose_name=_("ترم در چارت"),
        choices=_term_in_chart_choices(),
    )
    title = models.CharField(
        verbose_name=_("عنوان"),
        max_length=255,
    )
    en_title = models.CharField(
        verbose_name=_("عنوان به انگلیسی"),
        max_length=255,
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
        blank=True)
    type = models.CharField(
        verbose_name=_("نوع"),
        max_length=1,
        choices=TYPE_CHOICES,
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "درس"
        verbose_name_plural = "دروس"


class Session(models.Model):
    def _current_year():
        return jdatetime.date.today().year

    FALL = "FA"
    SPRING = "SP"
    SUMMER = "SU"

    SEMESTER_CHOICES = [
        (FALL, "اول"),
        (SPRING, "دوم"),
        (SUMMER, "تابستان"),
    ]

    year = models.PositiveSmallIntegerField(
        verbose_name=_("سال"),
        validators=[
            MinValueValidator(1300),
            MaxValueValidator(_current_year)
        ],
    )
    semester = models.CharField(
        verbose_name=_("نیم سال"),
        max_length=2,
        choices=SEMESTER_CHOICES,
    )
    course = models.ForeignKey(
        Course,
        verbose_name=_("درس"),
        on_delete=models.PROTECT,
    )

    def __str__(self) -> str:
        return f"{self.year} - {self.semester} - {self.course.en_title}"

    class Meta:
        verbose_name = "کلاس"
        verbose_name_plural = "کلاس‌ها"


class TA(models.Model):
    full_name = models.CharField(
        verbose_name=_("نام و نام خانوادگی"),
        max_length=255,
    )
    session = models.ForeignKey(
        Session,
        verbose_name=_("کلاس"),
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name = "گریدر"
        verbose_name_plural = "گریدرها"


class Resource(models.Model):
    MIDTERM = "M"
    FINAL = "F"
    HOMEWORK = "H"
    QUIZ = "Q"
    OTHER = "O"

    TYPE_CHOICES = [
        (MIDTERM, "میانترم"),
        (FINAL, "پایانترم"),
        (HOMEWORK, "تمرین"),
        (QUIZ, "کوییز"),
        (OTHER, "دیگر"),
    ]

    title = models.CharField(
        verbose_name=_("عنوان"),
        max_length=255,
    )
    url = models.URLField(
        verbose_name=_("لینک دانلود"),
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
    session = models.ForeignKey(
        Session,
        verbose_name=_("کلاس"),
        on_delete=models.PROTECT,
    )

    def __str__(self) -> str:
        return f"{self.session} - {self.title}"

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
