# Generated by Django 5.1.5 on 2025-02-11 14:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database_admin', '0007_alter_product_assigned_rfid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='assigned_rfid',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product', to='database_admin.rfidentry'),
        ),
    ]
