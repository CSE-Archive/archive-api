from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Reference(models.Model):
    cover_image = models.ImageField(upload_to="img/r/", blank=True)
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField()

    def __str__(self) -> str:
        return self.title


class Author(models.Model):
    full_name = models.CharField(max_length=255)
    reference = models.ForeignKey(
        Reference,
        on_delete=models.CASCADE,
        related_name="authors",
    )

    def __str__(self) -> str:
        return self.full_name


class ReferenceItem(models.Model):
    reference = models.ForeignKey(
        Reference,
        on_delete=models.CASCADE,
        related_name="reference_items",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="reference_items",
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self) -> str:
        return f"{self.content_object} - {self.reference}"
