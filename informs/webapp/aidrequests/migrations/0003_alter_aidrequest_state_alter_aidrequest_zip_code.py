# Generated by Django 5.1.3 on 2024-11-15 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aidrequests', '0002_alter_aidrequest_group_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aidrequest',
            name='state',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='aidrequest',
            name='zip_code',
            field=models.CharField(max_length=10),
        ),
    ]
