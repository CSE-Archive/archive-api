# Generated by Django 4.2.5 on 2023-10-02 17:21

import core.helpers
import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classrooms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', core.models.ShortUuidField(db_index=True, default=core.helpers.uuid_generator, editable=False, max_length=11, unique=True, verbose_name='UUID')),
                ('is_published', models.BooleanField(default=False, verbose_name='Is Published')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='Modified Time')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Title')),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Midterm'), (2, 'Final'), (3, 'Project'), (4, 'Homework'), (5, 'Quiz'), (6, 'Other')], verbose_name='Type')),
                ('notes', models.CharField(blank=True, max_length=255, null=True, verbose_name='Notes')),
                ('file', models.FileField(blank=True, max_length=255, null=True, upload_to='resources', verbose_name='File')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='resources', to='classrooms.classroom', verbose_name='Classroom')),
            ],
            options={
                'verbose_name': 'Resource',
                'verbose_name_plural': 'Resources',
                'ordering': ('-modified_time', '-created_time'),
            },
        ),
    ]
