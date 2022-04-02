# Generated by Django 4.0.3 on 2022-04-02 21:57

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
                ('unit', models.PositiveSmallIntegerField()),
                ('term_in_chart', models.PositiveSmallIntegerField()),
                ('title', models.CharField(max_length=255)),
                ('en_title', models.CharField(max_length=255)),
                ('tag', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('type', models.CharField(choices=[('B', 'Basic'), ('G', 'General'), ('O', 'Optional'), ('S', 'Specialized')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(choices=[('FA', 'Fall'), ('SP', 'Spring'), ('SU', 'Summer')], max_length=2)),
                ('year', models.PositiveSmallIntegerField(choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022)])),
            ],
        ),
        migrations.CreateModel(
            name='TA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.session')),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(choices=[('M', 'Midterm'), ('F', 'Final'), ('H', 'Homework'), ('Q', 'Quiz'), ('O', 'Other')], max_length=1)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='course.session')),
            ],
        ),
        migrations.CreateModel(
            name='Requisite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('C', 'Corequisite'), ('P', 'Prerequisite')], max_length=1)),
                ('course1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course1', to='course.course')),
                ('course2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course2', to='course.course')),
            ],
        ),
    ]