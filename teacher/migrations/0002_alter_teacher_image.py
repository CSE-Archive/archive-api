# Generated by Django 4.0.3 on 2022-04-06 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.ImageField(blank=True, upload_to='img/t/'),
        ),
    ]
