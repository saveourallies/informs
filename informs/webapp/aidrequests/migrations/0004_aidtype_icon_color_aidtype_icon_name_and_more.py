# Generated by Django 5.1.4 on 2025-01-14 16:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aidrequests', '0003_alter_aidtype_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='aidtype',
            name='icon_color',
            field=models.CharField(default='blue', max_length=7),
        ),
        migrations.AddField(
            model_name='aidtype',
            name='icon_name',
            field=models.CharField(choices=[('ambulance', 'Ambulance'), ('fire_truck', 'Fire Truck'), ('police_car', 'Police Car'), ('helicopter', 'Helicopter')], default='helicopter', max_length=20),
        ),
        migrations.AddField(
            model_name='aidtype',
            name='icon_scale',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=4, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)]),
        ),
    ]
