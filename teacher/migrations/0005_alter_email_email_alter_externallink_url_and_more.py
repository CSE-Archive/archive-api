# Generated by Django 4.0.3 on 2022-04-11 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_alter_email_teacher_alter_externallink_teacher_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='externallink',
            name='url',
            field=models.URLField(max_length=255, verbose_name='لینک'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='about',
            field=models.TextField(verbose_name='درباره'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='first_name',
            field=models.CharField(max_length=255, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.ImageField(blank=True, upload_to='img/t/', verbose_name='تصویر'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='last_name',
            field=models.CharField(max_length=255, verbose_name='نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='teacheritem',
            name='object_id',
            field=models.PositiveIntegerField(verbose_name='آی دی آبجکت'),
        ),
    ]
