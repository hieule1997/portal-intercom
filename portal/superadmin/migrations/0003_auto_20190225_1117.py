# Generated by Django 2.1.7 on 2019-02-25 04:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0002_auto_20190225_0857'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='state',
            new_name='region',
        ),
    ]