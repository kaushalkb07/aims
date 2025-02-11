# Generated by Django 5.1.5 on 2025-02-11 14:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database_admin', '0006_remove_product_last_updated_remove_rfidentry_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='assigned_rfid',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database_admin.rfidentry'),
        ),
    ]
