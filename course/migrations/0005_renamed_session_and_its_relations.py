from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_alter_resource_url'),
    ]

    operations = [
        migrations.RenameModel('Session', 'Classroom'),
        migrations.RenameField('TA', 'session', 'classroom'),
        migrations.RenameField('Resource', 'session', 'classroom')
    ]
