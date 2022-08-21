from .validators import image_size_validator
from django.db import models
from django.utils.translation import gettext as _


class Author(models.Model):
    full_name = models.CharField(
        verbose_name=_("نام و نام خانوادگی"),
        max_length=255,
    )

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name = "نویسنده"
        verbose_name_plural = "نویسندگان"


class Reference(models.Model):
    file = models.FileField(
        verbose_name=_("فایل"),
        upload_to="files/references/",
    )
    title = models.CharField(
        verbose_name=_("عنوان"),
        max_length=255,
    )
    date_created = models.DateTimeField(
        verbose_name=_("تاریخ اضافه شدن"),
        auto_now_add=True,
    )
    date_modified = models.DateTimeField(
        verbose_name=_("آخرین ویرایش"),
        auto_now=True,
    )
    support_url = models.URLField(
        verbose_name=_("لینک دانلود حمایتی"),
        max_length=255,
        blank=True,
        null=True,
    )
    cover_image = models.ImageField(
        verbose_name=_("تصویر جلد"),
        upload_to="images/references/",
        blank=True,
        validators=[image_size_validator],
    )
    authors = models.ManyToManyField(
        Author,
        related_name="references",
        verbose_name=_("نویسندگان"),
        blank=True,
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "مرجع"
        verbose_name_plural = "مراجع"
