# Generated by Django 5.1.3 on 2024-11-19 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aidrequests', '0005_aidlocation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aidlocation',
            old_name='notes',
            new_name='note',
        ),
    ]
