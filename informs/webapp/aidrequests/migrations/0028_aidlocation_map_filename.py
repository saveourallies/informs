# Generated by Django 5.1.4 on 2024-12-15 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aidrequests', '0027_aidlocation_address_found_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='aidlocation',
            name='map_filename',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
