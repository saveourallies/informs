# Generated by Django 5.1.5 on 2025-01-31 15:02

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aidrequests', '0005_alter_aidtype_icon_name'),
        ('takserver', '0002_takserver_notes_alter_takserver_cert_private_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldop',
            name='tak_server',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='field_ops', to='takserver.takserver'),
        ),
        migrations.AlterField(
            model_name='aidtype',
            name='icon_scale',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=4, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)]),
        ),
    ]
