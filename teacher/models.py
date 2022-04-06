from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Teacher(models.Model):
    image = models.ImageField(upload_to="img/t/", blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    about = models.TextField()

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Email(models.Model):
    email = models.EmailField(unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.email


class ExternalLink(models.Model):
    url = models.URLField(max_length=255)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.url


class TeacherItem(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self) -> str:
        return f"{self.content_object} - {self.teacher}"
