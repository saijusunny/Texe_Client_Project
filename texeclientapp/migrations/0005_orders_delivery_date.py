# Generated by Django 4.0.2 on 2024-01-03 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texeclientapp', '0004_orders_stage_alter_registration_joindate'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='delivery_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]