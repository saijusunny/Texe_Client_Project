# Generated by Django 4.0.2 on 2023-11-27 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texeclientapp', '0014_remove_orders_item_checkout_item_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='stage_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
