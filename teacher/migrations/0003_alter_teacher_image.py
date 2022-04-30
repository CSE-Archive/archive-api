# Generated by Django 4.0.4 on 2022-04-27 22:52

from django.db import migrations, models
import teacher.validators


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_teacher_department_alter_teacher_about'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.ImageField(blank=True, upload_to='img/t/', validators=[teacher.validators.image_size_validator], verbose_name='تصویر'),
        ),
    ]
