from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext as _
from django_jalali.db import models as jmodels


class Reference(models.Model):
    objects = jmodels.jManager()

    cover_image = models.ImageField(
        verbose_name=_("تصویر جلد"),
        upload_to="img/r/",
        blank=True,
    )
    title = models.CharField(
        verbose_name=_("عنوان"),
        max_length=255,
    )
    url = models.URLField(
        verbose_name=_("لینک دانلود"),
        max_length=255,
    )
    date_created = jmodels.jDateTimeField(
        verbose_name=_("تاریخ اضافه شدن"),
        auto_now_add=True,
    )
    date_modified = jmodels.jDateTimeField(
        verbose_name=_("آخرین ویرایش"),
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
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.full_name
    
    class Meta:
        verbose_name = "نویسنده"
        verbose_name_plural = "نویسنده‌ها"


class ReferenceItem(models.Model):
    reference = models.ForeignKey(
        Reference,
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
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
