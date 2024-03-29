# Generated by Django 4.2.5 on 2023-10-02 17:21

import core.helpers
import core.models
import django.core.validators
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
                ('title', models.CharField(max_length=127, verbose_name='Title')),
                ('en_title', models.CharField(blank=True, max_length=127, null=True, verbose_name='Title in English')),
                ('units', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3')], verbose_name='Units')),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Specialized'), (2, 'Optional'), (3, 'Basic'), (4, 'General')], verbose_name='Type')),
                ('tag', core.models.TagField(blank=True, max_length=127, null=True, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z\u0600-ۿ_]*$', 'Tags can only contain Persian and English letters and underscores.')], verbose_name='Tag')),
                ('known_as', models.CharField(blank=True, max_length=127, null=True, verbose_name='Known As')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
                'ordering': ('type', 'title'),
            },
        ),
        migrations.CreateModel(
            name='CourseRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Corequisite'), (2, 'Prerequisite'), (3, 'Incompatible')], verbose_name='Type')),
                ('course_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations_from', to='courses.course', verbose_name='Course From')),
                ('course_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations_to', to='courses.course', verbose_name='Course To')),
            ],
            options={
                'verbose_name': 'Course Relation',
                'verbose_name_plural': 'Course Relations',
            },
        ),
        migrations.AddConstraint(
            model_name='courserelation',
            constraint=models.UniqueConstraint(fields=('course_from', 'course_to'), name='unique_relation_reverse', violation_error_message='Two courses can have at most one relationship.'),
        ),
        migrations.AddConstraint(
            model_name='courserelation',
            constraint=models.CheckConstraint(check=models.Q(('course_from', models.F('course_to')), _negated=True), name='prevent_self_relation', violation_error_message='Courses cannot have a relationship to themselves.'),
        ),
    ]
