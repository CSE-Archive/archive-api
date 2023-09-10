# Generated by Django 4.2.4 on 2023-09-10 15:30

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
            name='RecordedClassroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', core.models.ShortUuidField(db_index=True, default=core.helpers.uuid_generator, editable=False, max_length=11, unique=True, verbose_name='UUID')),
                ('is_published', models.BooleanField(default=False, verbose_name='Is Published')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Created Time')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='Modified Time')),
                ('notes', models.CharField(max_length=255, null=True, verbose_name='Notes')),
                ('classroom', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='recordings', to='classrooms.classroom', verbose_name='Classroom')),
            ],
            options={
                'verbose_name': 'Recored Classroom',
                'verbose_name_plural': 'Recored Classrooms',
                'ordering': ('modified_time', 'created_time'),
            },
        ),
        migrations.CreateModel(
            name='RecordedSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('order', models.FloatField(verbose_name='Order')),
                ('recorded_classroom', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sessions', to='recordings.recordedclassroom', verbose_name='Recored Classroom')),
            ],
            options={
                'verbose_name': 'Recored Session',
                'verbose_name_plural': 'Recored Sessions',
                'ordering': ('order', 'id'),
            },
        ),
    ]
