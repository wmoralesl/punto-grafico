# Generated by Django 5.1.2 on 2025-02-06 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_design_offer_price_alter_design_on_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='design',
            name='name',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Descripción'),
        ),
    ]
