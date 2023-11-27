# Generated by Django 4.0.2 on 2023-11-27 07:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('texeclientapp', '0013_remove_checkout_item_item_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='item',
        ),
        migrations.AddField(
            model_name='checkout_item',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='texeclientapp.item'),
        ),
    ]
