# Generated by Django 5.1.5 on 2025-02-12 16:50

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database_admin', '0013_alter_stockmovement_timestamp_in_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockmovement',
            name='timestamp_in',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='stockmovement',
            name='timestamp_out',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
