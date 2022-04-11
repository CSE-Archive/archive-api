# Generated by Django 4.0.3 on 2022-04-10 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('reference', '0003_alter_reference_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='reference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authors', to='reference.reference'),
        ),
        migrations.AlterField(
            model_name='referenceitem',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reference_items', to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='referenceitem',
            name='reference',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reference_items', to='reference.reference'),
        ),
    ]
