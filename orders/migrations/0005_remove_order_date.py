# Generated by Django 5.1.2 on 2025-06-01 05:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_anticipo_order_created_order_deadline_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='date',
        ),
    ]
