# Generated by Django 5.1.4 on 2025-01-13 12:14

import django.db.models.deletion
import informs.utils
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldOpNotify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('email-individual', 'Email Individual'), ('email-group', 'Email Group'), ('sms', 'SMS')], max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('sms_number', models.CharField(blank=True, max_length=15, null=True)),
            ],
            options={
                'verbose_name': 'Notify Address',
                'verbose_name_plural': 'Notify Addresses',
            },
        ),
        migrations.CreateModel(
            name='AidRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('requestor_first_name', models.CharField(max_length=20)),
                ('requestor_last_name', models.CharField(max_length=30)),
                ('requestor_email', models.EmailField(blank=True, max_length=254)),
                ('requestor_phone', models.CharField(blank=True, max_length=12)),
                ('assistance_first_name', models.CharField(blank=True, max_length=20)),
                ('assistance_last_name', models.CharField(blank=True, max_length=30)),
                ('assistance_email', models.EmailField(blank=True, max_length=254)),
                ('assistance_phone', models.CharField(blank=True, max_length=12)),
                ('street_address', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=25)),
                ('state', models.CharField(max_length=20)),
                ('zip_code', models.CharField(blank=True, max_length=10)),
                ('country', models.CharField(blank=True, max_length=30)),
                ('assistance_type', models.CharField(choices=[('evacuation', 'Evacuation'), ('re_supply', 'Re-supply'), ('welfare_check', 'Welfare check'), ('other', 'Other')], max_length=20)),
                ('assistance_description', models.TextField(blank=True, null=True)),
                ('group_size', models.PositiveIntegerField(blank=True, null=True)),
                ('contact_methods', models.TextField(blank=True, null=True)),
                ('medical_needs', models.TextField(blank=True, null=True)),
                ('supplies_needed', models.TextField(blank=True, null=True)),
                ('welfare_check_info', models.TextField(blank=True, null=True)),
                ('additional_info', models.TextField(blank=True, null=True)),
                ('priority', models.CharField(blank=True, choices=[(None, 'None'), ('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], default=None, max_length=10, null=True)),
                ('status', models.CharField(choices=[('new', 'New'), ('assigned', 'Assigned'), ('resolved', 'Resolved'), ('closed', 'Closed'), ('rejected', 'Rejected'), ('other', 'Other')], default='new', max_length=10)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aid_requests_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aid_requests_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Aid Request',
                'verbose_name_plural': 'Aid Requests',
            },
        ),
        migrations.CreateModel(
            name='AidLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uid', models.CharField(default=informs.utils.takuid_new, max_length=36, unique=True)),
                ('status', models.CharField(choices=[('new', 'New'), ('confirmed', 'Confirmed'), ('rejected', 'Rejected'), ('candidate', 'Candidate'), ('other', 'Other')], max_length=10)),
                ('latitude', models.DecimalField(decimal_places=5, max_digits=8)),
                ('longitude', models.DecimalField(decimal_places=5, max_digits=9)),
                ('source', models.CharField(choices=[('manual', 'Manual'), ('azure_maps', 'Azure Maps'), ('other', 'Other')], max_length=20)),
                ('note', models.TextField(blank=True, null=True)),
                ('address_searched', models.CharField(blank=True, max_length=100, null=True)),
                ('address_found', models.CharField(blank=True, max_length=100, null=True)),
                ('distance', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('map_filename', models.CharField(blank=True, max_length=100, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aid_locations_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aid_locations_updated', to=settings.AUTH_USER_MODEL)),
                ('aid_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='aidrequests.aidrequest')),
            ],
            options={
                'verbose_name': 'Aid Location',
                'verbose_name_plural': 'Aid Locations',
            },
        ),
        migrations.CreateModel(
            name='AidRequestLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('log_entry', models.TextField()),
                ('aid_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='aidrequests.aidrequest')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aid_request_logs_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='aid_request_logs_updated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Aid Request Log',
                'verbose_name_plural': 'Aid Request Logs',
            },
        ),
        migrations.CreateModel(
            name='FieldOp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=50)),
                ('latitude', models.DecimalField(decimal_places=5, max_digits=7)),
                ('longitude', models.DecimalField(decimal_places=5, max_digits=8)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='field_ops_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='field_ops_updated', to=settings.AUTH_USER_MODEL)),
                ('notify', models.ManyToManyField(to='aidrequests.fieldopnotify')),
            ],
            options={
                'verbose_name': 'Field Operation',
                'verbose_name_plural': 'Field Operations',
            },
        ),
        migrations.AddField(
            model_name='aidrequest',
            name='field_op',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aid_requests', to='aidrequests.fieldop'),
        ),
    ]
