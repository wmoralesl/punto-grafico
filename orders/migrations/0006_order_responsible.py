# Generated by Django 5.1.2 on 2025-06-01 17:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
        ('orders', '0005_remove_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='responsible',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='employee.employee'),
        ),
    ]
