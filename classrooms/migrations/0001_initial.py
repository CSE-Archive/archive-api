# Generated by Django 4.2.5 on 2023-09-29 16:52

import core.helpers
import core.models
import core.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('professors', '0001_initial'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', core.models.ShortUuidField(db_index=True, default=core.helpers.uuid_generator, editable=False, max_length=11, unique=True, verbose_name='UUID')),
                ('full_name', models.CharField(max_length=255, unique=True, verbose_name='Full Name')),
            ],
            options={
                'verbose_name': 'TA',
                'verbose_name_plural': 'TAs',
                'ordering': ('full_name',),
            },
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', core.models.ShortUuidField(db_index=True, default=core.helpers.uuid_generator, editable=False, max_length=11, unique=True, verbose_name='UUID')),
                ('is_published', models.BooleanField(default=False, verbose_name='Is Published')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='Modified Time')),
                ('year', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1300), core.validators.MaxCurrentYearValidator()], verbose_name='Year')),
                ('semester', models.PositiveSmallIntegerField(choices=[(1, 'First'), (2, 'Second'), (3, 'Summer')], verbose_name='Semester')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='classrooms', to='courses.course', verbose_name='Course')),
                ('professors', models.ManyToManyField(blank=True, related_name='classrooms', to='professors.professor', verbose_name='Professors')),
                ('tas', models.ManyToManyField(blank=True, related_name='classrooms', to='classrooms.ta', verbose_name='TAs')),
            ],
            options={
                'verbose_name': 'Classroom',
                'verbose_name_plural': 'Classrooms',
                'ordering': ('-year', '-semester', 'course__type', 'course__title'),
            },
        ),
    ]
