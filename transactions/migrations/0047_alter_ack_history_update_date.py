# Generated by Django 4.1.5 on 2024-03-24 11:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0046_alter_ack_history_update_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ack_history',
            name='update_date',
            field=models.DateField(blank=True, default=datetime.datetime(2024, 3, 24, 11, 34, 11, 213558, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]