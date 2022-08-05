from .validators import image_size_validator
from django.db import models
from django.utils.translation import gettext as _


class Teacher(models.Model):
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
    image = models.ImageField(
        verbose_name=_("تصویر"),
        upload_to="images/teachers/",
        blank=True,
        validators=[image_size_validator],
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
        related_name="emails",
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
        related_name="external_links",
    )

    def __str__(self) -> str:
        return self.url

    class Meta:
        verbose_name = "لینک"
        verbose_name_plural = "لینک‌ها"
