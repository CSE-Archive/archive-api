from .validators import image_size_validator
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from gdstorage.storage import GoogleDriveStorage


gd_storage = GoogleDriveStorage()


class Reference(models.Model):
    url = models.FileField(
        verbose_name=_("فایل"),
        upload_to="files/references/",
        storage=gd_storage,
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
        storage=gd_storage,
        blank=True,
        validators=[image_size_validator],
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "مرجع"
        verbose_name_plural = "مراجع"


class Author(models.Model):
    full_name = models.CharField(
        verbose_name=_("نام و نام خانوادگی"),
        max_length=255,
    )
    reference = models.ForeignKey(
        Reference,
        verbose_name=_("مرجع"),
        on_delete=models.CASCADE,
        related_name="authors",
    )

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name = "نویسنده"
        verbose_name_plural = "نویسنده‌ها"


class ReferenceItem(models.Model):
    reference = models.ForeignKey(
        Reference,
        verbose_name=_("مرجع"),
        on_delete=models.CASCADE,
        related_name="reference_items",
    )
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_("نوع محتوا"),
        on_delete=models.CASCADE,
        related_name="reference_items",
    )
    object_id = models.PositiveIntegerField(
        verbose_name=_("آی دی آبجکت"),
    )
    content_object = GenericForeignKey()

    def __str__(self) -> str:
        return f"{self.content_object} - {self.reference}"

    class Meta:
        verbose_name = "رابط مرجع"
        verbose_name_plural = "رابط‌های مراجع"
