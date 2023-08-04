# Generated by Django 4.2.3 on 2023-08-04 15:12

import core.helpers
import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', core.models.ShortUuidField(db_index=True, default=core.helpers.uuid_generator, editable=False, max_length=11, unique=True, verbose_name='UUID')),
                ('is_published', models.BooleanField(default=False, verbose_name='Is Published')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='Modified Time')),
                ('title', models.CharField(blank=True, max_length=127, verbose_name='Title')),
                ('en_title', models.CharField(blank=True, max_length=127, verbose_name='Title in English')),
                ('unit', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3')], verbose_name='Unit')),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Specialized'), (2, 'Optional'), (3, 'Basic'), (4, 'General')], verbose_name='Type')),
                ('tag', models.CharField(blank=True, max_length=127, verbose_name='Tag')),
                ('known_as', models.CharField(blank=True, max_length=127, verbose_name='Known As')),
                ('description', models.TextField(blank=True, default='', verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
                'ordering': ('type', 'title'),
            },
        ),
        migrations.CreateModel(
            name='Requisite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Corequisite'), (2, 'Prerequisite')], verbose_name='Type')),
                ('course_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requisites_from', to='courses.course', verbose_name='Course From')),
                ('course_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requisites_to', to='courses.course', verbose_name='Course To')),
            ],
            options={
                'verbose_name': 'Requisite',
                'verbose_name_plural': 'Requisities',
                'unique_together': {('course_from', 'course_to')},
            },
        ),
    ]
