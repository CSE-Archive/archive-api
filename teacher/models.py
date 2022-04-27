from django.db import models
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .validators import image_size_validator


class Teacher(models.Model):
    image = models.ImageField(
        verbose_name=_("تصویر"),
        upload_to="img/t/",
        blank=True,
        validators=[image_size_validator],
    )
    first_name = models.CharField(
        verbose_name=_("نام"),
        max_length=255,
    )
    last_name = models.CharField(
        verbose_name=_("نام خانوادگی"),
        max_length=255,
    )
    department = models.CharField(
        verbose_name=_("بخش"),
        max_length=8,
    )
    about = models.TextField(
        verbose_name=_("درباره"),
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "استاد"
        verbose_name_plural = "اساتید"


class Email(models.Model):
    email = models.EmailField(
        verbose_name=_("ایمیل"),
        unique=True,
    )
    teacher = models.ForeignKey(
        Teacher,
        verbose_name=_("استاد"),
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.email

    class Meta:
        verbose_name = "ایمیل"
        verbose_name_plural = "ایمیل‌ها"


class ExternalLink(models.Model):
    url = models.URLField(
        verbose_name=_("لینک"),
        max_length=255,
    )
    teacher = models.ForeignKey(
        Teacher,
        verbose_name=_("استاد"),
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.url

    class Meta:
        verbose_name = "لینک"
        verbose_name_plural = "لینک‌ها"


class TeacherItem(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        verbose_name=_("استاد"),
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_("نوع محتوا"),
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_("آی دی آبجکت"),
    )
    content_object = GenericForeignKey()

    def __str__(self) -> str:
        return f"{self.content_object} - {self.teacher}"

    class Meta:
        verbose_name = "رابط استاد"
        verbose_name_plural = "رابط‌های اساتید"
