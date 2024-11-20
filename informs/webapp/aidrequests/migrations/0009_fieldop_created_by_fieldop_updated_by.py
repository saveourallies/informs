# Generated by Django 5.1.3 on 2024-11-20 15:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aidrequests', '0008_aidlocation_created_at_aidlocation_updated_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldop',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='field_ops_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fieldop',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='field_ops_updated', to=settings.AUTH_USER_MODEL),
        ),
    ]
