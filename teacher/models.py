from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Teacher(models.Model):
    image = models.ImageField(upload_to="images/t/%Y/%m/%d", blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    about = models.TextField()


class Email(models.Model):
    email = models.EmailField(unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)


class ExternalLink(models.Model):
    url = models.URLField(max_length=255)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

class TeacherItem(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()    
