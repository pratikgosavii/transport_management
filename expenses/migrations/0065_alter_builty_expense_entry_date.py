# Generated by Django 3.2.15 on 2024-04-13 22:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0064_merge_20240414_0321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='builty_expense',
            name='entry_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]
